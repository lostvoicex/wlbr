#!/usr/bin/env bash
# 沙盒开发/试跑启动：切换到 vite preview（生产静态包）以规避
# @vitejs/plugin-vue@5.2.4 dev 模式 transformStyle bug。
# 流程：后端 uvicorn (8000) 后台 + 前端 pnpm build 一次 + pnpm preview 前台常驻。
# 沙盒 supervisor 挂在最后 exec 的进程上，preview 死了才会重启（此时会自动再 build 一次）。
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

# 载入 .env（如果存在）
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

echo "[start-dev][preview 模式] 后端 FastAPI :${BACKEND_PORT}，前端 vite preview :${DEPLOY_RUN_PORT}"

# --- 后端 ---
cd "${ROOT_DIR}/backend"
# 首次启动自动 seed（幂等）
python -m app.seed >> "${LOG_DIR}/app.log" 2>&1 || echo "[start-dev] seed 跳过或已存在"
# 如果 uvicorn 已在监听 BACKEND_PORT，跳过重新启动
if ! ss -lptn "sport = :${BACKEND_PORT}" 2>/dev/null | grep -q LISTEN; then
  nohup uvicorn app.main:app --host 0.0.0.0 --port "${BACKEND_PORT}" \
    >> "${LOG_DIR}/app.log" 2>&1 &
  echo "[start-dev] backend pid=$!"
else
  echo "[start-dev] backend 已监听 :${BACKEND_PORT}，跳过重启"
fi

# --- 前端 build（保证 dist 最新） ---
cd "${ROOT_DIR}/frontend"
echo "[start-dev] pnpm build ..."
pnpm build >> "${LOG_DIR}/dev.log" 2>&1 || {
  echo "[start-dev] build 失败，查看 ${LOG_DIR}/dev.log"
  exit 1
}

# --- 前端 preview（前台，供 supervisor 挂着） ---
echo "[start-dev] pnpm preview --host 0.0.0.0 --port ${DEPLOY_RUN_PORT}"
exec pnpm preview --host 0.0.0.0 --port "${DEPLOY_RUN_PORT}"
