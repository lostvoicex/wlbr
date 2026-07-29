"""KP 映射相关 schemas。"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class KpMappingBase(BaseModel):
    syllabus_version: str = Field(..., max_length=32)
    knowledge_point: str = Field(..., max_length=128)
    courseware_name: str = Field(..., max_length=255)
    chapter: str = Field(..., max_length=64)
    page_ref: Optional[str] = Field(None, max_length=64)
    chapter_title: Optional[str] = Field(None, max_length=255)
    match_score: int = Field(default=0, ge=0, le=100)
    source: str = Field(default="manual", pattern=r"^(ai|manual|import)$")
    review_status: str = Field(default="pending", pattern=r"^(pending|approved|rejected|needs_review)$")
    review_level: int = Field(default=1, ge=1, le=5)
    is_active: bool = True
    sort_order: int = 0


class KpMappingCreate(KpMappingBase):
    pass


class KpMappingUpdate(BaseModel):
    courseware_name: Optional[str] = Field(None, max_length=255)
    chapter: Optional[str] = Field(None, max_length=64)
    page_ref: Optional[str] = Field(None, max_length=64)
    chapter_title: Optional[str] = Field(None, max_length=255)
    match_score: Optional[int] = Field(None, ge=0, le=100)
    source: Optional[str] = Field(None, pattern=r"^(ai|manual|import)$")
    review_status: Optional[str] = Field(None, pattern=r"^(pending|approved|rejected|needs_review)$")
    review_level: Optional[int] = Field(None, ge=1, le=5)
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


class KpMappingOut(KpMappingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reviewer1_id: Optional[int] = None
    reviewer2_id: Optional[int] = None
    review_note: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class KpMappingListResp(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[KpMappingOut]


class ReviewRequest(BaseModel):
    """审核请求：一审或二审。"""
    result: str = Field(..., pattern=r"^(approved|rejected|needs_review)$")
    review_level: int = Field(default=1, ge=1, le=5)
    note: Optional[str] = Field(None, description="审核备注")


class MappingReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    mapping_id: int
    reviewer_id: Optional[int] = None
    reviewer_name: Optional[str] = None
    review_round: int
    result: str
    review_level: int
    note: Optional[str] = None
    created_at: datetime


# ---------- 批量导入 ----------

class MappingImportItem(BaseModel):
    """单条映射导入项。"""
    syllabus_version: str
    knowledge_point: str
    courseware_name: str
    chapter: str
    page_ref: Optional[str] = None
    chapter_title: Optional[str] = None
    match_score: int = 0
    source: str = "import"
    sort_order: int = 0


class MappingImportResult(BaseModel):
    """批量导入结果。"""
    total: int
    success: int
    failed: int
    errors: List[str] = []
    imported_ids: List[int] = []
