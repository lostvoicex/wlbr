"""FastAPI 主入口。"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_v1_router
from app.config import settings
from app.db import Base, engine

# 引入模型以确保 Base.metadata 感知到所有表（Alembic 迁移也依赖它）
from app import models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    """启动钩子：sqlite dev 模式下自动 create_all（生产环境请走 Alembic 迁移）。"""
    if settings.database_url.startswith("sqlite"):
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="面向 2-6 年级少儿编程学员的查缺补漏诊断平台 · M1 骨架",
    lifespan=lifespan,
)

_allowed_origins = settings.cors_origins_list
if not _allowed_origins:
    raise RuntimeError(
        "CORS_ALLOW_ORIGINS 未配置，请设置环境变量。"
        "开发环境示例：http://localhost:5000,http://127.0.0.1:5000"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)


@app.api_route("/api/health", methods=["GET", "HEAD"], tags=["meta"], summary="健康检查")
def health() -> dict:
    from sqlalchemy import text as sa_text
    from app.db import SessionLocal

    db_ok = True
    try:
        db = SessionLocal()
        db.execute(sa_text("SELECT 1"))
        db.close()
    except Exception:
        db_ok = False

    return {
        "status": "ok" if db_ok else "degraded",
        "app": settings.app_name,
        "env": settings.app_env,
        "db": "ok" if db_ok else "error",
        "version": "0.1.0",
    }


app.include_router(api_v1_router)
