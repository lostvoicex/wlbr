#!/usr/bin/env bash
# 后端启动脚本（Render 生产环境用）
# 功能：1) 转换 DATABASE_URL 格式  2) 建表/迁移  3) 种子数据  4) 启动 FastAPI

set -e

echo "========== 瓦力贝尔后端启动 =========="

# Render 提供的 DATABASE_URL 是 postgres://，需转换为 postgresql+psycopg://
if [ -n "$DATABASE_URL" ]; then
  export DATABASE_URL="${DATABASE_URL/postgres:\/\//postgresql+psycopg:\/\/}"
  echo "数据库连接串: $DATABASE_URL"
fi

# 确保 SQLite 数据目录存在
mkdir -p ./data

# 建表策略：
# - PostgreSQL：用 Alembic 迁移（BigInteger 在 PG 中支持 autoincrement）
# - SQLite：用 create_all（ORM 的 BigInteger().with_variant(Integer, "sqlite") 才能让 autoincrement 生效）
if [ -n "$DATABASE_URL" ]; then
  echo "使用 PostgreSQL，执行 Alembic 迁移..."
  alembic upgrade head || echo "WARNING: 迁移失败，将使用 create_all 兜底"
else
  echo "使用 SQLite，跳过 Alembic（避免 BigInteger 导致 autoincrement 失效）"
fi

# 用 create_all 兜底（确保表存在，已存在则跳过）
echo "确保表结构存在..."
python -c "
from app.db import Base, engine
from app import models  # noqa: F401 - 触发模型注册
Base.metadata.create_all(bind=engine)
print('表结构就绪')
"

# 检查是否已有种子数据，没有则初始化
echo "检查种子数据..."
SEED_CHECK=$(python -c "
from app.db import SessionLocal
from app.models.question import Question
db = SessionLocal()
count = db.query(Question).count()
print(count)
db.close()
" 2>/dev/null || echo "0")

if [ "$SEED_CHECK" = "0" ]; then
  echo "首次部署，初始化演示数据（486题 + 5位学员）..."
  python -m app.seed
  echo "种子数据初始化完成"
else
  echo "已有 $SEED_CHECK 道题目，跳过种子数据初始化"
fi

# 启动 FastAPI（Koyeb/Render 都通过 PORT 环境变量指定端口）
PORT="${PORT:-8000}"
echo "启动服务，端口: $PORT"
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
