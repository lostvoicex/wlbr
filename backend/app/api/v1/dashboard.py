"""仪表盘统计路由：/api/v1/dashboard/*"""
from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.deps import CurrentUser, require_role
from app.db import get_db
from app.models import DiagnosisSession, KpMasterySnapshot, Student, Teacher, WorkOrder

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _resolve_teacher_id(user: CurrentUser, db: Session) -> int | None:
    if user.role not in ("teacher", "admin"):
        return None
    teacher = db.query(Teacher).filter(Teacher.teacher_no == user.subject).first()
    return teacher.id if teacher else None


class StatCard(BaseModel):
    label: str
    value: int
    sub: str | None = None


class SessionTypeStat(BaseModel):
    session_type: str
    count: int


class WorkOrderStat(BaseModel):
    status: str
    count: int


class MasteryStat(BaseModel):
    mastery_level: str
    count: int


class RecentActivity(BaseModel):
    session_id: int
    student_id: int
    student_name: str
    session_type: str
    syllabus_target: str
    correct_count: int
    total_count: int
    status: str
    suspicious_flag: bool
    started_at: datetime


class DashboardResp(BaseModel):
    student_total: int
    student_new_this_week: int
    session_total: int
    session_finished: int
    session_in_progress: int
    suspicious_count: int
    work_order_pending: int
    work_order_in_progress: int
    work_order_completed: int
    session_type_stats: List[SessionTypeStat]
    work_order_stats: List[WorkOrderStat]
    mastery_stats: List[MasteryStat]
    recent_activities: List[RecentActivity]


@router.get(
    "/stats",
    response_model=DashboardResp,
    summary="仪表盘统计数据（老师/管理员）",
)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_role("teacher", "admin")),
) -> DashboardResp:
    now = datetime.now(tz=timezone.utc)
    week_ago = now - timedelta(days=7)

    teacher_id = _resolve_teacher_id(user, db)

    # --- 学员统计 ---
    student_total = db.query(Student).count()
    student_new_this_week = (
        db.query(Student)
        .filter(Student.created_at >= week_ago)
        .count()
    )

    # --- 诊断会话统计 ---
    session_total = db.query(DiagnosisSession).count()
    session_finished = (
        db.query(DiagnosisSession)
        .filter(DiagnosisSession.status == "finished")
        .count()
    )
    session_in_progress = (
        db.query(DiagnosisSession)
        .filter(DiagnosisSession.status == "in_progress")
        .count()
    )
    suspicious_count = (
        db.query(DiagnosisSession)
        .filter(DiagnosisSession.suspicious_flag == True)  # noqa: E712
        .count()
    )

    # 按类型统计
    type_rows = (
        db.query(
            DiagnosisSession.session_type,
            func.count(DiagnosisSession.id).label("cnt"),
        )
        .group_by(DiagnosisSession.session_type)
        .all()
    )
    session_type_stats = [
        SessionTypeStat(session_type=r.session_type, count=r.cnt)
        for r in type_rows
    ]

    # --- 工单统计 ---
    wo_query = db.query(WorkOrder)
    if user.role == "teacher" and teacher_id is not None:
        wo_query = wo_query.filter(WorkOrder.assignee_id == teacher_id)

    wo_rows = (
        wo_query.with_entities(
            WorkOrder.status,
            func.count(WorkOrder.id).label("cnt"),
        )
        .group_by(WorkOrder.status)
        .all()
    )
    wo_stat_map = {r.status: r.cnt for r in wo_rows}
    work_order_stats = [
        WorkOrderStat(status=s, count=wo_stat_map.get(s, 0))
        for s in ("pending", "in_progress", "completed", "cancelled")
    ]

    # --- KP 掌握度分布 ---
    mastery_rows = (
        db.query(
            KpMasterySnapshot.mastery_level,
            func.count(KpMasterySnapshot.id).label("cnt"),
        )
        .group_by(KpMasterySnapshot.mastery_level)
        .all()
    )
    mastery_stats = [
        MasteryStat(mastery_level=r.mastery_level, count=r.cnt)
        for r in mastery_rows
    ]

    # --- 最近活动 ---
    recent_sessions = (
        db.query(DiagnosisSession, Student.name)
        .join(Student, DiagnosisSession.student_id == Student.id)
        .order_by(DiagnosisSession.started_at.desc())
        .limit(10)
        .all()
    )
    recent_activities = [
        RecentActivity(
            session_id=s.id,
            student_id=s.student_id,
            student_name=name,
            session_type=s.session_type,
            syllabus_target=s.syllabus_target,
            correct_count=s.correct_count,
            total_count=s.total_count,
            status=s.status,
            suspicious_flag=s.suspicious_flag,
            started_at=s.started_at,
        )
        for s, name in recent_sessions
    ]

    return DashboardResp(
        student_total=student_total,
        student_new_this_week=student_new_this_week,
        session_total=session_total,
        session_finished=session_finished,
        session_in_progress=session_in_progress,
        suspicious_count=suspicious_count,
        work_order_pending=wo_stat_map.get("pending", 0),
        work_order_in_progress=wo_stat_map.get("in_progress", 0),
        work_order_completed=wo_stat_map.get("completed", 0),
        session_type_stats=session_type_stats,
        work_order_stats=work_order_stats,
        mastery_stats=mastery_stats,
        recent_activities=recent_activities,
    )
