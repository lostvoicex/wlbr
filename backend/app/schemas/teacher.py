"""老师相关 schemas。"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class TeacherBase(BaseModel):
    teacher_no: str = Field(..., min_length=1, max_length=32)
    name: str = Field(..., min_length=1, max_length=64)
    role: str = Field(default="teacher", pattern=r"^(teacher|admin)$")
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=128)
    status: str = Field(default="active", pattern=r"^(active|disabled)$")


class TeacherCreate(TeacherBase):
    password: str = Field(..., min_length=4, max_length=64)


class TeacherUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=64)
    role: Optional[str] = Field(None, pattern=r"^(teacher|admin)$")
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=128)
    status: Optional[str] = Field(None, pattern=r"^(active|disabled)$")
    password: Optional[str] = Field(None, min_length=4, max_length=64)


class TeacherOut(TeacherBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class TeacherListResp(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[TeacherOut]
