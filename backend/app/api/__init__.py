"""API v1 路由聚合。"""
from fastapi import APIRouter

from app.api.v1 import (
    admin_data,
    auth,
    copy_texts,
    diagnosis_sessions,
    kp_labels,
    kp_mappings,
    oj,
    questions,
    reminders,
    students,
    teachers,
    work_orders,
)

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(auth.router)
api_v1_router.include_router(students.router)
api_v1_router.include_router(questions.router)
api_v1_router.include_router(diagnosis_sessions.router)
api_v1_router.include_router(kp_labels.router)
api_v1_router.include_router(copy_texts.router)
api_v1_router.include_router(reminders.router)
api_v1_router.include_router(teachers.router)
api_v1_router.include_router(work_orders.router)
api_v1_router.include_router(kp_mappings.router)
api_v1_router.include_router(admin_data.router)
api_v1_router.include_router(oj.router)

__all__ = ["api_v1_router"]
