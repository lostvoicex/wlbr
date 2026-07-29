#!/usr/bin/env bash
# 生产启动：后端 uvicorn + 用 pnpm preview 提供前端静态资源
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi

: "${DEPLOY_RUN_PORT:=5000}"
: "${BACKEND_PORT:=8000}"
export DEPLOY_RUN_PORT BACKEND_PORT

LOG_DIR="/app/work/logs/bypass/"
mkdir -p "${LOG_DIR}" 2>/dev/null || LOG_DIR="${ROOT_DIR}/logs"
mkdir -p "${LOG_DIR}"

echo "[start-prod] 后端 :${BACKEND_PORT}，前端 :${DEPLOY_RUN_PORT}"

cd "${ROOT_DIR}/backend"
python -m app.seed >> "${LOG_DIR}/app.log" 2>&1 || true
nohup uvicorn app.main:app --host 0.0.0.0 --port "${BACKEND_PORT}" \
  >> "${LOG_DIR}/app.log" 2>&1 &

cd "${ROOT_DIR}/frontend"
exec pnpm preview --host 0.0.0.0 --port "${DEPLOY_RUN_PORT}"
