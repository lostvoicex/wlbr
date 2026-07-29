"""复测提醒 / 老师催办接口。

数据来自 kp_mastery_snapshots：
- 学员端：查该学员所有 need_review / need_repair 快照，按天数筛出 T1/T2 到期提醒
- 老师端：跨全体学员聚合到期项，返回催办列表
"""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.constants import REMINDERS_T1, REMINDERS_T2
from app.core.deps import CurrentUser, get_current_user, require_role
from app.db import get_db
from app.models import DiagnosisSession, KpMasterySnapshot, Student

router = APIRouter(tags=["reminders"])


class ReminderItem(BaseModel):
    kp_original: str
    mastery_level: str  # need_review / need_repair
    retest_type: str  # t1 / t2
    days_ago: int
    last_snapshot_at: datetime
    correct_rate: float
    syllabus_target: str


class StudentRemindersResp(BaseModel):
    student_id: int
    total: int
    t1_items: List[ReminderItem]
    t2_items: List[ReminderItem]


class TeacherAlertItem(BaseModel):
    student_id: int
    student_name: str
    kp_original: str
    mastery_level: str
    retest_type: str  # t1 / t2
    days_ago: int
    last_snapshot_at: datetime


class TeacherAlertsResp(BaseModel):
    total: int
    items: List[TeacherAlertItem]


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _days_ago(dt: datetime) -> int:
    now = _now_utc()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    delta = now - dt
    return max(delta.days, 0)


def _pick_latest_per_kp(
    snapshots: List[KpMasterySnapshot],
) -> Dict[str, KpMasterySnapshot]:
    """每个 KP 只保留 created_at 最新的一条快照。"""
    latest: Dict[str, KpMasterySnapshot] = {}
    for s in snapshots:
        cur = latest.get(s.knowledge_point)
        if cur is None or s.created_at > cur.created_at:
            latest[s.knowledge_point] = s
    return latest


@router.get(
    "/student-reminders",
    response_model=StudentRemindersResp,
    summary="学员端：读取自己的 T1/T2 复测到期提醒",
)
def get_student_reminders(
    student_id: Optional[int] = Query(
        None, description="管理端联调时可显式指定，学生角色忽略此字段"
    ),
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
) -> StudentRemindersResp:
    if user.role == "student":
        try:
            sid = int(user.subject)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="登录信息无效"
            )
    else:
        if student_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="老师/管理员访问需要指定 student_id",
            )
        sid = student_id

    snaps = (
        db.query(KpMasterySnapshot)
        .filter(KpMasterySnapshot.student_id == sid)
        .filter(KpMasterySnapshot.mastery_level.in_(["need_review", "need_repair"]))
        .all()
    )
    latest = _pick_latest_per_kp(snaps)

    # 获取 session_id -> syllabus_target 映射
    session_ids = {s.session_id for s in snaps}
    sessions: Dict[int, str] = {}
    if session_ids:
        for sess in db.query(DiagnosisSession).filter(DiagnosisSession.id.in_(session_ids)).all():
            sessions[sess.id] = sess.syllabus_target

    t1_items: List[ReminderItem] = []
    t2_items: List[ReminderItem] = []
    for kp, s in latest.items():
        d = _days_ago(s.created_at)
        syllabus = sessions.get(s.session_id, "scratch-l1")
        if s.mastery_level == "need_review" and d >= REMINDERS_T1["days"]:
            t1_items.append(
                ReminderItem(
                    kp_original=kp,
                    mastery_level=s.mastery_level,
                    retest_type="t1",
                    days_ago=d,
                    last_snapshot_at=s.created_at,
                    correct_rate=float(s.correct_rate),
                    syllabus_target=syllabus,
                )
            )
        elif s.mastery_level == "need_repair" and d >= REMINDERS_T2["days"]:
            t2_items.append(
                ReminderItem(
                    kp_original=kp,
                    mastery_level=s.mastery_level,
                    retest_type="t2",
                    days_ago=d,
                    last_snapshot_at=s.created_at,
                    correct_rate=float(s.correct_rate),
                    syllabus_target=syllabus,
                )
            )

    t1_items.sort(key=lambda x: x.days_ago, reverse=True)
    t2_items.sort(key=lambda x: x.days_ago, reverse=True)

    return StudentRemindersResp(
        student_id=sid,
        total=len(t1_items) + len(t2_items),
        t1_items=t1_items,
        t2_items=t2_items,
    )


@router.get(
    "/teacher-alerts",
    response_model=TeacherAlertsResp,
    summary="老师端：全体学员的复测催办列表",
)
def get_teacher_alerts(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _=Depends(require_role("teacher", "admin")),
) -> TeacherAlertsResp:
    snaps = (
        db.query(KpMasterySnapshot)
        .filter(KpMasterySnapshot.mastery_level.in_(["need_review", "need_repair"]))
        .all()
    )

    # 按 (student_id, kp) 只保留最新一条
    latest_key: Dict[tuple, KpMasterySnapshot] = {}
    for s in snaps:
        key = (s.student_id, s.knowledge_point)
        cur = latest_key.get(key)
        if cur is None or s.created_at > cur.created_at:
            latest_key[key] = s

    items: List[TeacherAlertItem] = []
    student_cache: Dict[int, Optional[str]] = {}
    for (sid, kp), s in latest_key.items():
        d = _days_ago(s.created_at)
        if s.mastery_level == "need_review" and d < REMINDERS_T1["days"]:
            continue
        if s.mastery_level == "need_repair" and d < REMINDERS_T2["days"]:
            continue

        if sid not in student_cache:
            stu = db.query(Student).filter(Student.id == sid).first()
            student_cache[sid] = stu.name if stu else None
        name = student_cache[sid] or f"学员#{sid}"

        retest_type = "t1" if s.mastery_level == "need_review" else "t2"
        items.append(
            TeacherAlertItem(
                student_id=sid,
                student_name=name,
                kp_original=kp,
                mastery_level=s.mastery_level,
                retest_type=retest_type,
                days_ago=d,
                last_snapshot_at=s.created_at,
            )
        )

    items.sort(key=lambda x: x.days_ago, reverse=True)
    items = items[:limit]

    return TeacherAlertsResp(total=len(items), items=items)
