"""补课工单相关 schemas。"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class WorkOrderBase(BaseModel):
    student_id: int
    session_id: Optional[int] = None
    syllabus_target: str = Field(..., max_length=32)
    weak_kps: str = Field(..., description="薄弱知识点，多个用英文逗号分隔")
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    chapters_json: Optional[str] = None
    status: str = Field(default="pending", pattern=r"^(pending|in_progress|completed|cancelled)$")
    priority: str = Field(default="medium", pattern=r"^(low|medium|high)$")
    due_date: Optional[datetime] = None


class WorkOrderCreate(WorkOrderBase):
    assignee_id: Optional[int] = Field(None, description="被分配处理工单的老师ID（admin可指定）")


class WorkOrderUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    chapters_json: Optional[str] = None
    status: Optional[str] = Field(None, pattern=r"^(pending|in_progress|completed|cancelled)$")
    priority: Optional[str] = Field(None, pattern=r"^(low|medium|high)$")
    due_date: Optional[datetime] = None
    weak_kps: Optional[str] = None
    assignee_id: Optional[int] = Field(None, description="重新分配给另一位老师（仅admin）")


class WorkOrderOut(WorkOrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    teacher_id: Optional[int] = None
    assignee_id: Optional[int] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class WorkOrderDetail(WorkOrderOut):
    """工单详情，包含学员姓名等关联信息。"""
    student_name: Optional[str] = None
    teacher_name: Optional[str] = None
    assignee_name: Optional[str] = None


class WorkOrderListResp(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[WorkOrderOut]
