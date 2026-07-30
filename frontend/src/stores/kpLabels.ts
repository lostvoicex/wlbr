#!/usr/bin/env bash
# 后端启动脚本（Render 生产环境用）
# 功能：1) 转换 DATABASE_URL 格式  2) 执行 Alembic 迁移  3) 启动 FastAPI

set -e

echo "========== 瓦力贝尔后端启动 =========="

# Render 提供的 DATABASE_URL 是 postgres://，需转换为 postgresql+psycopg://
if [ -n "$DATABASE_URL" ]; then
  export DATABASE_URL="${DATABASE_URL/postgres:\/\//postgresql+psycopg:\/\/}"
  echo "数据库连接串: $DATABASE_URL"
fi

# 确保 SQLite 数据目录存在
mkdir -p ./data

# 执行 Alembic 迁移（自动升级到最新版本）
echo "执行数据库迁移..."
alembic upgrade head

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
