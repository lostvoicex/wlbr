"""题库路由：/api/v1/questions/*"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_role
from app.db import get_db
from app.models import Question
from app.schemas.question import QuestionListResp, QuestionOut

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get(
    "",
    response_model=QuestionListResp,
    summary="题库列表（分页 + 过滤，供老师/管理员使用）",
)
def list_questions(
    db: Session = Depends(get_db),
    _=Depends(require_role("teacher", "admin")),
    syllabus_version: Optional[str] = Query(None),
    grade_level: Optional[int] = Query(None, ge=1, le=6),
    q_type: Optional[str] = Query(None, pattern="^(single|judge|coding|program)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> QuestionListResp:
    q = db.query(Question)
    if syllabus_version:
        q = q.filter(Question.syllabus_version == syllabus_version)
    if grade_level is not None:
        q = q.filter(Question.grade_level == grade_level)
    if q_type:
        q = q.filter(Question.q_type == q_type)

    total = q.count()
    items = (
        q.order_by(Question.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return QuestionListResp(
        total=total,
        page=page,
        page_size=page_size,
        items=[QuestionOut.model_validate(x) for x in items],
    )


@router.get(
    "/random",
    response_model=list[QuestionOut],
    summary="学员诊断抽题（M1 骨架：按大纲+级别随机取 10 道，混排三型）",
)
def random_pick(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
    syllabus_version: str = Query(..., description="如 scratch-l1 / scratch-l2"),
    grade_level: int = Query(..., ge=1, le=6),
    count: int = Query(10, ge=1, le=30),
) -> list[QuestionOut]:
    # SQLite 与 PostgreSQL 都支持 RANDOM() 函数
    from sqlalchemy import func as sa_func

    rows = (
        db.query(Question)
        .filter(
            Question.syllabus_version == syllabus_version,
            Question.grade_level == grade_level,
        )
        .order_by(sa_func.random())
        .limit(count)
        .all()
    )
    return [QuestionOut.model_validate(x) for x in rows]


@router.get(
    "/{question_id}",
    response_model=QuestionOut,
    summary="题目详情",
)
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
) -> QuestionOut:
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="题目不存在")
    return QuestionOut.model_validate(q)
