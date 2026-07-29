"""补课工单管理路由：/api/v1/work-orders/*"""
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import CurrentUser, get_current_user, require_role
from app.db import get_db
from app.models import Student, Teacher, WorkOrder
from app.schemas.work_order import (
    WorkOrderCreate,
    WorkOrderDetail,
    WorkOrderListResp,
    WorkOrderOut,
    WorkOrderUpdate,
)

router = APIRouter(prefix="/work-orders", tags=["work-orders"])


def _resolve_teacher_id(user: CurrentUser, db: Session) -> int | None:
    """根据当前登录用户（teacher_no）解析出 teacher.id。"""
    if user.role not in ("teacher", "admin"):
        return None
    teacher = db.query(Teacher).filter(Teacher.teacher_no == user.subject).first()
    return teacher.id if teacher else None


def _require_work_order_access(
    work_order_id: int,
    user: CurrentUser,
    db: Session,
    allow_admin: bool = True,
) -> WorkOrder:
    """校验当前用户是否有权访问指定工单。

    - admin：始终有权（当 allow_admin=True）
    - teacher：仅当 assignee_id 等于自己时有权
    """
    wo = db.query(WorkOrder).filter(WorkOrder.id == work_order_id).first()
    if not wo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="工单不存在")

    if user.role == "admin" and allow_admin:
        return wo

    # teacher 只能访问分配给自己的工单
    teacher_id = _resolve_teacher_id(user, db)
    if teacher_id is not None and wo.assignee_id == teacher_id:
        return wo

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="没有权限操作该工单",
    )


@router.get(
    "",
    response_model=WorkOrderListResp,
    summary="工单列表（分页 + 筛选）",
)
def list_work_orders(
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_role("teacher", "admin")),
    student_id: Optional[int] = Query(None, description="按学员ID筛选"),
    status: Optional[str] = Query(
        None, pattern=r"^(pending|in_progress|completed|cancelled)$", description="按状态筛选"
    ),
    priority: Optional[str] = Query(
        None, pattern=r"^(low|medium|high)$", description="按优先级筛选"
    ),
    syllabus_target: Optional[str] = Query(None, description="按大纲目标筛选"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> WorkOrderListResp:
    q = db.query(WorkOrder)

    # 权限过滤：普通教师只能看自己分配的工单
    if user.role == "teacher":
        teacher_id = _resolve_teacher_id(user, db)
        if teacher_id:
            q = q.filter(WorkOrder.assignee_id == teacher_id)
        else:
            # 找不到教师记录，返回空
            return WorkOrderListResp(total=0, page=page, page_size=page_size, items=[])

    if student_id is not None:
        q = q.filter(WorkOrder.student_id == student_id)
    if status:
        q = q.filter(WorkOrder.status == status)
    if priority:
        q = q.filter(WorkOrder.priority == priority)
    if syllabus_target:
        q = q.filter(WorkOrder.syllabus_target == syllabus_target)

    total = q.count()
    items = (
        q.order_by(WorkOrder.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return WorkOrderListResp(
        total=total,
        page=page,
        page_size=page_size,
        items=[WorkOrderOut.model_validate(w) for w in items],
    )


@router.post(
    "",
    response_model=WorkOrderOut,
    status_code=status.HTTP_201_CREATED,
    summary="创建工单（老师/管理员）",
)
def create_work_order(
    payload: WorkOrderCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_role("teacher", "admin")),
) -> WorkOrderOut:
    # 校验学员是否存在
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="学员不存在"
        )

    # 从当前登录用户获取 teacher_id（teacher_no -> teacher.id）
    teacher_id = _resolve_teacher_id(user, db)

    # 处理 assignee_id
    assignee_id = payload.assignee_id
    if user.role == "teacher":
        # 普通教师只能把工单分配给自己
        assignee_id = teacher_id
    elif user.role == "admin" and assignee_id:
        # admin 指定了分配人，校验该教师是否存在
        assigned_teacher = db.query(Teacher).filter(Teacher.id == assignee_id).first()
        if not assigned_teacher:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="指定的分配教师不存在"
            )

    work_order = WorkOrder(
        student_id=payload.student_id,
        session_id=payload.session_id,
        teacher_id=teacher_id,
        assignee_id=assignee_id,
        syllabus_target=payload.syllabus_target,
        weak_kps=payload.weak_kps,
        title=payload.title,
        description=payload.description,
        chapters_json=payload.chapters_json,
        status=payload.status,
        priority=payload.priority,
        due_date=payload.due_date,
    )
    db.add(work_order)
    db.commit()
    db.refresh(work_order)
    return WorkOrderOut.model_validate(work_order)


@router.get(
    "/{work_order_id}",
    response_model=WorkOrderDetail,
    summary="工单详情（含学员姓名、老师姓名）",
)
def get_work_order(
    work_order_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_role("teacher", "admin")),
) -> WorkOrderDetail:
    work_order = _require_work_order_access(work_order_id, user, db)

    # 关联查询学员姓名和老师姓名
    student_name = None
    teacher_name = None
    assignee_name = None

    student = db.query(Student).filter(Student.id == work_order.student_id).first()
    if student:
        student_name = student.name

    if work_order.teacher_id:
        teacher = db.query(Teacher).filter(Teacher.id == work_order.teacher_id).first()
        if teacher:
            teacher_name = teacher.name

    if work_order.assignee_id:
        assignee = db.query(Teacher).filter(Teacher.id == work_order.assignee_id).first()
        if assignee:
            assignee_name = assignee.name

    detail = WorkOrderDetail.model_validate(work_order)
    detail.student_name = student_name
    detail.teacher_name = teacher_name
    detail.assignee_name = assignee_name
    return detail


@router.put(
    "/{work_order_id}",
    response_model=WorkOrderOut,
    summary="更新工单",
)
def update_work_order(
    work_order_id: int,
    payload: WorkOrderUpdate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_role("teacher", "admin")),
) -> WorkOrderOut:
    work_order = _require_work_order_access(work_order_id, user, db)

    update_data = payload.model_dump(exclude_unset=True)

    # 普通教师不能重新分配工单
    if user.role == "teacher" and "assignee_id" in update_data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有教学主管可以重新分配工单",
        )

    # admin 重新分配时校验目标教师
    if user.role == "admin" and "assignee_id" in update_data and update_data["assignee_id"]:
        assigned_teacher = db.query(Teacher).filter(
            Teacher.id == update_data["assignee_id"]
        ).first()
        if not assigned_teacher:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="指定的分配教师不存在"
            )

    for field, value in update_data.items():
        setattr(work_order, field, value)

    db.commit()
    db.refresh(work_order)
    return WorkOrderOut.model_validate(work_order)


@router.delete(
    "/{work_order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="取消工单（设置 status=cancelled）",
)
def cancel_work_order(
    work_order_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_role("teacher", "admin")),
) -> None:
    work_order = _require_work_order_access(work_order_id, user, db)
    work_order.status = "cancelled"
    db.commit()


@router.post(
    "/{work_order_id}/complete",
    response_model=WorkOrderOut,
    summary="标记工单完成",
)
def complete_work_order(
    work_order_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_role("teacher", "admin")),
) -> WorkOrderOut:
    work_order = _require_work_order_access(work_order_id, user, db)
    if work_order.status == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="已取消的工单不能标记完成"
        )
    work_order.status = "completed"
    work_order.completed_at = datetime.now(tz=timezone.utc)
    db.commit()
    db.refresh(work_order)
    return WorkOrderOut.model_validate(work_order)
