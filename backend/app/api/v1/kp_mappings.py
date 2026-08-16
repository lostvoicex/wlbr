"""KP 映射管理路由：/api/v1/kp-mappings/*"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.deps import CurrentUser, require_role
from app.db import get_db
from app.models import KpMapping, MappingReview, Teacher
from app.schemas.kp_mapping import (
    KpMappingCreate,
    KpMappingListResp,
    KpMappingOut,
    KpMappingUpdate,
    MappingReviewOut,
    ReviewRequest,
)

router = APIRouter(prefix="/kp-mappings", tags=["kp-mappings"])


def _resolve_teacher_id(user: CurrentUser, db: Session) -> int | None:
    """根据当前登录用户（teacher_no）解析出 teacher.id。"""
    if user.role not in ("teacher", "admin"):
        return None
    teacher = db.query(Teacher).filter(Teacher.teacher_no == user.subject).first()
    return teacher.id if teacher else None


@router.get(
    "",
    response_model=KpMappingListResp,
    summary="映射列表（分页 + 筛选）",
)
def list_kp_mappings(
    db: Session = Depends(get_db),
    _=Depends(require_role("teacher", "admin")),
    syllabus_version: Optional[str] = Query(None, description="按大纲版本筛选"),
    knowledge_point: Optional[str] = Query(None, description="按知识点模糊搜索"),
    courseware_name: Optional[str] = Query(None, description="按课件名称模糊搜索"),
    review_status: Optional[str] = Query(
        None,
        pattern=r"^(pending|approved|rejected|needs_review)$",
        description="按审核状态筛选",
    ),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> KpMappingListResp:
    q = db.query(KpMapping)
    if syllabus_version:
        q = q.filter(KpMapping.syllabus_version == syllabus_version)
    if knowledge_point:
        like = f"%{knowledge_point.strip()}%"
        q = q.filter(KpMapping.knowledge_point.like(like))
    if courseware_name:
        like = f"%{courseware_name.strip()}%"
        q = q.filter(KpMapping.courseware_name.like(like))
    if review_status:
        q = q.filter(KpMapping.review_status == review_status)

    total = q.count()
    items = (
        q.order_by(KpMapping.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return KpMappingListResp(
        total=total,
        page=page,
        page_size=page_size,
        items=[KpMappingOut.model_validate(m) for m in items],
    )


@router.post(
    "",
    response_model=KpMappingOut,
    status_code=status.HTTP_201_CREATED,
    summary="新建映射",
)
def create_kp_mapping(
    payload: KpMappingCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("teacher", "admin")),
) -> KpMappingOut:
    mapping = KpMapping(
        syllabus_version=payload.syllabus_version,
        knowledge_point=payload.knowledge_point,
        courseware_name=payload.courseware_name,
        chapter=payload.chapter,
        page_ref=payload.page_ref,
        chapter_title=payload.chapter_title,
        match_score=payload.match_score,
        source=payload.source,
        review_status=payload.review_status,
        review_level=payload.review_level,
        is_active=payload.is_active,
        sort_order=payload.sort_order,
    )
    db.add(mapping)
    db.commit()
    db.refresh(mapping)
    return KpMappingOut.model_validate(mapping)


@router.get(
    "/{mapping_id}",
    response_model=KpMappingOut,
    summary="映射详情",
)
def get_kp_mapping(
    mapping_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("teacher", "admin")),
) -> KpMappingOut:
    mapping = db.query(KpMapping).filter(KpMapping.id == mapping_id).first()
    if not mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="映射不存在"
        )
    return KpMappingOut.model_validate(mapping)


@router.put(
    "/{mapping_id}",
    response_model=KpMappingOut,
    summary="更新映射",
)
def update_kp_mapping(
    mapping_id: int,
    payload: KpMappingUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_role("teacher", "admin")),
) -> KpMappingOut:
    mapping = db.query(KpMapping).filter(KpMapping.id == mapping_id).first()
    if not mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="映射不存在"
        )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(mapping, field, value)

    db.commit()
    db.refresh(mapping)
    return KpMappingOut.model_validate(mapping)


@router.delete(
    "/{mapping_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除映射",
)
def delete_kp_mapping(
    mapping_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("admin")),
) -> None:
    mapping = db.query(KpMapping).filter(KpMapping.id == mapping_id).first()
    if not mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="映射不存在"
        )
    db.delete(mapping)
    db.commit()


@router.post(
    "/{mapping_id}/review",
    response_model=KpMappingOut,
    summary="提交审核（一审/二审自动判断当前是第几审）",
)
def review_kp_mapping(
    mapping_id: int,
    payload: ReviewRequest,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_role("teacher", "admin")),
) -> KpMappingOut:
    mapping = db.query(KpMapping).filter(KpMapping.id == mapping_id).first()
    if not mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="映射不存在"
        )

    reviewer_id = _resolve_teacher_id(user, db)
    if reviewer_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无法解析教师身份，请联系管理员",
        )

    if mapping.reviewer1_id is not None and mapping.reviewer2_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该映射已完成二审，不可再次审核",
        )

    if mapping.reviewer1_id is None:
        review_round = 1
        mapping.reviewer1_id = reviewer_id
    else:
        if mapping.reviewer1_id == reviewer_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="一审审核人不可兼任二审，请由其他老师进行二审",
            )
        review_round = 2
        mapping.reviewer2_id = reviewer_id

    # 更新映射的审核状态和等级
    mapping.review_status = payload.result
    mapping.review_level = payload.review_level
    mapping.review_note = payload.note

    # 写入审核记录
    review = MappingReview(
        mapping_id=mapping.id,
        reviewer_id=reviewer_id,
        review_round=review_round,
        result=payload.result,
        review_level=payload.review_level,
        note=payload.note,
    )
    db.add(review)

    db.commit()
    db.refresh(mapping)
    return KpMappingOut.model_validate(mapping)


@router.get(
    "/{mapping_id}/reviews",
    response_model=list[MappingReviewOut],
    summary="获取审核记录列表",
)
def get_mapping_reviews(
    mapping_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role("teacher", "admin")),
) -> list[MappingReviewOut]:
    mapping = db.query(KpMapping).filter(KpMapping.id == mapping_id).first()
    if not mapping:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="映射不存在"
        )

    reviews = (
        db.query(MappingReview)
        .filter(MappingReview.mapping_id == mapping_id)
        .order_by(MappingReview.id.asc())
        .all()
    )

    result = []
    for r in reviews:
        review_out = MappingReviewOut.model_validate(r)
        # 填充审核人姓名
        if r.reviewer_id:
            teacher = db.query(Teacher).filter(Teacher.id == r.reviewer_id).first()
            if teacher:
                review_out.reviewer_name = teacher.name
        result.append(review_out)
    return result
