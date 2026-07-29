"""知识点掌握度算法。

阈值定义（M1）：
- correct_rate >= 0.8   → mastered      （已掌握）
- 0.5 <= correct_rate <  0.8 → need_review  （需要再练练）
- correct_rate <  0.5   → need_repair   （需要重点补的）

若某 KP 只有 1-2 题，标 low_confidence=True 但仍按上述阈值判定。
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

MASTERED_THRESHOLD = Decimal("0.8")
REVIEW_THRESHOLD = Decimal("0.5")
LOW_CONFIDENCE_MAX_TOTAL = 2  # total_count <= 2 视为低置信


@dataclass
class KpAggregate:
    knowledge_point: str
    correct_count: int
    total_count: int
    correct_rate: Decimal
    mastery_level: str  # mastered / need_review / need_repair
    low_confidence: bool


def classify(correct_rate: Decimal) -> str:
    """按阈值把正确率映射到三档掌握度。"""
    if correct_rate >= MASTERED_THRESHOLD:
        return "mastered"
    if correct_rate >= REVIEW_THRESHOLD:
        return "need_review"
    return "need_repair"


def aggregate_by_kp(
    records: Iterable[tuple[str, bool | None]],
) -> list[KpAggregate]:
    """把 (knowledge_point, is_correct) 列表聚合成每个 KP 的 KpAggregate。"""
    bucket: dict[str, list[bool]] = {}
    for kp, is_correct in records:
        if not kp:
            continue
        bucket.setdefault(kp, []).append(bool(is_correct))

    result: list[KpAggregate] = []
    for kp, hits in bucket.items():
        total = len(hits)
        correct = sum(1 for h in hits if h)
        rate = (
            Decimal(correct) / Decimal(total)
            if total > 0
            else Decimal("0")
        ).quantize(Decimal("0.0001"))
        result.append(
            KpAggregate(
                knowledge_point=kp,
                correct_count=correct,
                total_count=total,
                correct_rate=rate,
                mastery_level=classify(rate),
                low_confidence=total <= LOW_CONFIDENCE_MAX_TOTAL,
            )
        )
    # 需要重点补的排在最前，其次需要再练练，最后已掌握
    order = {"need_repair": 0, "need_review": 1, "mastered": 2}
    result.sort(key=lambda x: (order.get(x.mastery_level, 9), -x.total_count))
    return result
