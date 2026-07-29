"""KP 童趣化命名接口：前端启动时拉一次即可，无需鉴权。"""
from typing import Dict, List

from fastapi import APIRouter
from pydantic import BaseModel

from app.constants import KP_LABELS

router = APIRouter(prefix="/kp-labels", tags=["kp-labels"])


class KpLabelOut(BaseModel):
    original_name: str
    display_name: str
    description: str


class KpLabelsResponse(BaseModel):
    total: int
    items: List[KpLabelOut]
    # 便于前端直接按原名 O(1) 取值
    map: Dict[str, KpLabelOut]


@router.get("", response_model=KpLabelsResponse, summary="拉取全部 KP 童趣化命名映射")
def list_kp_labels() -> KpLabelsResponse:
    items = [KpLabelOut(**v) for v in KP_LABELS.values()]
    mp = {v["original_name"]: KpLabelOut(**v) for v in KP_LABELS.values()}
    return KpLabelsResponse(total=len(items), items=items, map=mp)
