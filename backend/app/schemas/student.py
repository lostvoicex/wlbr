"""学员相关 schemas。"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
    grade: int = Field(..., ge=2, le=6)
    phone: Optional[str] = Field(None, max_length=20)
    syllabus_target: Optional[str] = Field(None, max_length=32)
    learning_note: Optional[str] = Field(None, max_length=50)


class StudentCreate(StudentBase):
    password: Optional[str] = Field(None, min_length=4, max_length=64)


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=64)
    grade: Optional[int] = Field(None, ge=2, le=6)
    phone: Optional[str] = Field(None, max_length=20)
    syllabus_target: Optional[str] = Field(None, max_length=32)
    learning_note: Optional[str] = Field(None, max_length=50)
    password: Optional[str] = Field(None, min_length=4, max_length=64)


class StudentOut(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class StudentListResp(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[StudentOut]


class KpSnapshotOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    knowledge_point: str
    correct_count: int
    total_count: int
    correct_rate: Decimal
    mastery_level: str


class SessionHistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_type: str
    syllabus_target: str
    total_count: int
    correct_count: int
    status: str
    started_at: datetime
    finished_at: Optional[datetime]
    suspicious_flag: bool
    suspicious_reason: Optional[str]
    kp_snapshots: List[KpSnapshotOut] = []


class SessionHistoryResp(BaseModel):
    total: int
    items: List[SessionHistoryOut]
