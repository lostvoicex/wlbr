"""业务常量模块（KP 童趣化命名、文案常量等）。"""
from .copy_texts import (
    BADGES,
    LOW_CONFIDENCE_SUFFIX,
    REMINDERS_T1,
    REMINDERS_T2,
    TEACHER_ALERTS,
    get_all_copy_texts,
)
from .kp_labels import KP_LABELS, get_kp_label

__all__ = [
    "KP_LABELS",
    "get_kp_label",
    "BADGES",
    "LOW_CONFIDENCE_SUFFIX",
    "REMINDERS_T1",
    "REMINDERS_T2",
    "TEACHER_ALERTS",
    "get_all_copy_texts",
]
