#!/usr/bin/env bash
# 后端启动脚本（Render 生产环境用）
# 功能：1) 转换 DATABASE_URL 格式  2) 执行 Alembic 迁移  3) 启动 FastAPI

set -e

echo "========== 瓦力贝尔后端启动 =========="

# Render 提供的 DATABASE_URL 是 postgres://，需转换为 postgresql+psycopg://
if [ -n "$DATABASE_URL" ]; then
  export DATABASE_URL="${DATABASE_URL/postgres:\/\//postgresql+psycopg:\/\/}"
  echo "数据库连接串已转换"
fi

# 执行 Alembic 迁移（自动升级到最新版本）
echo "执行数据库迁移..."
alembic upgrade head

# 如果是首次部署，可取消下面注释来初始化种子数据
# echo "初始化演示数据..."
# python -m app.seed

# 启动 FastAPI（Render 要求监听 0.0.0.0:$PORT）
PORT="${PORT:-10000}"
echo "启动服务，端口: $PORT"
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
