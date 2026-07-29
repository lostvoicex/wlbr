"""文案常量接口：前端启动时拉一次即可，无需鉴权。"""
from typing import Any, Dict

from fastapi import APIRouter

from app.constants import get_all_copy_texts

router = APIRouter(prefix="/copy-texts", tags=["copy-texts"])


@router.get("", summary="拉取全部展示文案（徽章 / 复测提醒 / 老师催办）")
def list_copy_texts() -> Dict[str, Any]:
    return get_all_copy_texts()
