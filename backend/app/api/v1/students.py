"""学员管理路由：/api/v1/students/*"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.deps import require_role
from app.core.security import hash_password, verify_password
from app.db import get_db
from app.models import DiagnosisSession, KpMasterySnapshot, Student
from app.schemas.student import (
    SessionHistoryOut,
    SessionHistoryResp,
    StudentCreate,
    StudentListResp,
    StudentOut,
    StudentUpdate,
)

router = APIRouter(prefix="/students", tags=["students"])


@router.get(
    "",
    response_model=StudentListResp,
    summary="学员列表（老师端使用，分页 + 搜索）",
)
def list_students(
    db: Session = Depends(get_db),
    _=Depends(require_role("teacher", "admin")),
    keyword: Optional[str] = Query(None, description="按姓名或手机号模糊搜索"),
    grade: Optional[int] = Query(None, ge=2, le=6),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> StudentListResp:
    q = db.query(Student)
    if keyword:
        like = f"%{keyword.strip()}%"
        q = q.filter(or_(Student.name.like(like), Student.phone.like(like)))
    if grade is not None:
        q = q.filter(Student.grade == grade)

    total = q.count()
    items = (
        q.order_by(Student.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return StudentListResp(
        total=total,
        page=page,
        page_size=page_size,
        items=[StudentOut.model_validate(s) for s in items],
    )


@router.post(
    "",
    response_model=StudentOut,
    status_code=status.HTTP_201_CREATED,
    summary="新建学员（老师/管理员）",
)
def create_student(
    payload: StudentCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("teacher", "admin")),
) -> StudentOut:
    if payload.phone:
        exists = db.query(Student).filter(Student.phone == payload.phone).first()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="该手机号已被注册"
            )
    student = Student(
        name=payload.name,
        grade=payload.grade,
        phone=payload.phone,
        syllabus_target=payload.syllabus_target,
        password_hash=hash_password(payload.password) if payload.password else None,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return StudentOut.model_validate(student)


@router.get(
    "/{student_id}",
    response_model=StudentOut,
    summary="学员详情",
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("teacher", "admin")),
) -> StudentOut:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="学员不存在")
    return StudentOut.model_validate(student)


@router.put(
    "/{student_id}",
    response_model=StudentOut,
    summary="更新学员信息（老师/管理员）",
)
def update_student(
    student_id: int,
    payload: StudentUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_role("teacher", "admin")),
) -> StudentOut:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="学员不存在")

    if payload.name is not None:
        student.name = payload.name
    if payload.grade is not None:
        student.grade = payload.grade
    if payload.phone is not None:
        if payload.phone:
            exists = (
                db.query(Student)
                .filter(Student.phone == payload.phone, Student.id != student_id)
                .first()
            )
            if exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="该手机号已被其他学员注册"
                )
        student.phone = payload.phone
    if payload.syllabus_target is not None:
        student.syllabus_target = payload.syllabus_target
    if payload.learning_note is not None:
        student.learning_note = payload.learning_note
    if payload.password:
        student.password_hash = hash_password(payload.password)

    db.commit()
    db.refresh(student)
    return StudentOut.model_validate(student)


@router.get(
    "/{student_id}/sessions",
    response_model=SessionHistoryResp,
    summary="学员诊断历史（老师端查看）",
)
def get_student_sessions(
    student_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("teacher", "admin")),
) -> SessionHistoryResp:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="学员不存在")

    sessions = (
        db.query(DiagnosisSession)
        .filter(DiagnosisSession.student_id == student_id)
        .order_by(DiagnosisSession.started_at.desc())
        .all()
    )

    items: list[SessionHistoryOut] = []
    for s in sessions:
        snapshots = (
            db.query(KpMasterySnapshot)
            .filter(KpMasterySnapshot.session_id == s.id)
            .all()
        )
        items.append(
            SessionHistoryOut(
                id=s.id,
                session_type=s.session_type,
                syllabus_target=s.syllabus_target,
                total_count=s.total_count,
                correct_count=s.correct_count,
                status=s.status,
                started_at=s.started_at,
                finished_at=s.finished_at,
                suspicious_flag=s.suspicious_flag,
                suspicious_reason=s.suspicious_reason,
                kp_snapshots=snapshots,
            )
        )

    return SessionHistoryResp(total=len(items), items=items)
