"""老师管理路由：/api/v1/teachers/*"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.deps import require_role
from app.core.security import hash_password
from app.db import get_db
from app.models import Teacher
from app.schemas.teacher import TeacherCreate, TeacherListResp, TeacherOut, TeacherUpdate

router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.get(
    "",
    response_model=TeacherListResp,
    summary="老师列表（分页 + 搜索，仅管理员）",
)
def list_teachers(
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
    keyword: Optional[str] = Query(None, description="按工号或姓名模糊搜索"),
    role: Optional[str] = Query(None, pattern=r"^(teacher|admin)$"),
    status: Optional[str] = Query(None, pattern=r"^(active|disabled)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=500),
) -> TeacherListResp:
    q = db.query(Teacher)
    if keyword:
        like = f"%{keyword.strip()}%"
        q = q.filter(or_(Teacher.teacher_no.like(like), Teacher.name.like(like)))
    if role:
        q = q.filter(Teacher.role == role)
    if status:
        q = q.filter(Teacher.status == status)

    total = q.count()
    items = (
        q.order_by(Teacher.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return TeacherListResp(
        total=total,
        page=page,
        page_size=page_size,
        items=[TeacherOut.model_validate(t) for t in items],
    )


@router.post(
    "",
    response_model=TeacherOut,
    status_code=status.HTTP_201_CREATED,
    summary="新建老师（仅管理员）",
)
def create_teacher(
    payload: TeacherCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
) -> TeacherOut:
    exists = db.query(Teacher).filter(Teacher.teacher_no == payload.teacher_no).first()
    if exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="该工号已被使用"
        )
    teacher = Teacher(
        teacher_no=payload.teacher_no,
        name=payload.name,
        role=payload.role,
        phone=payload.phone,
        email=payload.email,
        status=payload.status,
        password_hash=hash_password(payload.password),
    )
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return TeacherOut.model_validate(teacher)


@router.get(
    "/{teacher_id}",
    response_model=TeacherOut,
    summary="老师详情",
)
def get_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("teacher", "admin")),
) -> TeacherOut:
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="老师不存在")
    return TeacherOut.model_validate(teacher)


@router.put(
    "/{teacher_id}",
    response_model=TeacherOut,
    summary="更新老师（仅管理员）",
)
def update_teacher(
    teacher_id: int,
    payload: TeacherUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
) -> TeacherOut:
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="老师不存在")

    update_data = payload.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password_hash"] = hash_password(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(teacher, field, value)

    db.commit()
    db.refresh(teacher)
    return TeacherOut.model_validate(teacher)


@router.delete(
    "/{teacher_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除老师（软删除，设置 status=disabled，仅管理员）",
)
def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
) -> None:
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="老师不存在")
    teacher.status = "disabled"
    db.commit()
