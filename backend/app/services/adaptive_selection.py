"""自适应智能抽题算法。

根据学员历史掌握度（加权结果）动态分配各 KP 的题量：
- need_repair（红色）：高权重，多抽题（×2.5）
- need_review（黄色）：中权重，正常抽题（×1.5）
- mastered（绿色）：低权重，少抽题（×0.5）
- 无历史数据：等权分配

保证：
1. 每个有题库的 KP 至少 1 道题（总题数充足时）
2. 题目不重复
3. 难度分布尽量均衡
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List, Tuple

from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session

from app.models import Question
from app.services.retest_weighting import (
    WeightedKpResult,
    calculate_weighted_mastery,
)

# 各掌握档的抽题权重
WEIGHTS = {
    "need_repair": Decimal("2.5"),
    "need_review": Decimal("1.5"),
    "mastered": Decimal("0.5"),
    "unknown": Decimal("1.0"),  # 无历史数据
}

# 每个 KP 最少抽 1 道
MIN_PER_KP = 1


@dataclass
class KpAllocation:
    knowledge_point: str
    allocated: int  # 分配到的题数
    mastery_level: str
    weight: Decimal


def _kp_question_counts(
    db: Session, syllabus_target: str, kps: List[str]
) -> Dict[str, int]:
    """查询每个 KP 的可用题数。"""
    rows = (
        db.query(Question.knowledge_point, sa_func.count(Question.id))
        .filter(Question.syllabus_version == syllabus_target)
        .filter(Question.knowledge_point.in_(kps))
        .group_by(Question.knowledge_point)
        .all()
    )
    return {kp: cnt for kp, cnt in rows}


def _allocate_counts(
    total: int,
    kp_weights: Dict[str, Decimal],
    kp_avail: Dict[str, int],
) -> List[KpAllocation]:
    """按权重分配题数到各 KP。

    算法：
    1. 每个 KP 先保底 MIN_PER_KP 道（不超过可用题数）
    2. 剩余名额按权重比例分配
    3. 取整后多余的名额按权重从高到低逐题补
    """
    if not kp_weights:
        return []

    # 第一步：保底
    allocations: Dict[str, KpAllocation] = {}
    remaining = total
    for kp, weight in kp_weights.items():
        avail = kp_avail.get(kp, 0)
        base = min(MIN_PER_KP, avail)
        allocations[kp] = KpAllocation(
            knowledge_point=kp,
            allocated=base,
            mastery_level="unknown",
            weight=weight,
        )
        remaining -= base

    # 剩余名额按权重分配
    if remaining > 0:
        total_weight = sum(w for kp, w in kp_weights.items() if kp_avail.get(kp, 0) > MIN_PER_KP)
        if total_weight > 0:
            # 计算各 KP 应得的额外题数（向下取整）
            extras: Dict[str, int] = {}
            used = 0
            sorted_kps = sorted(
                kp_weights.items(),
                key=lambda x: x[1],
                reverse=True,
            )
            for kp, weight in sorted_kps:
                avail = kp_avail.get(kp, 0)
                max_extra = max(0, avail - MIN_PER_KP)
                if max_extra <= 0:
                    extras[kp] = 0
                    continue
                share = int((weight / total_weight * remaining).to_integral_value())
                share = min(share, max_extra)
                extras[kp] = share
                used += share

            # 还有剩余名额，按权重从高到低补
            leftover = remaining - used
            for kp, _ in sorted_kps:
                if leftover <= 0:
                    break
                avail = kp_avail.get(kp, 0)
                current = allocations[kp].allocated + extras.get(kp, 0)
                if current < avail:
                    extras[kp] = extras.get(kp, 0) + 1
                    leftover -= 1

            for kp, extra in extras.items():
                allocations[kp].allocated += extra

    return list(allocations.values())


def adaptive_select_questions(
    db: Session,
    student_id: int,
    syllabus_target: str,
    count: int,
) -> List[Question]:
    """自适应抽题：根据学员历史掌握度智能分配各 KP 题量。

    1. 查学员加权掌握度
    2. 查该 syllabus 下所有有题的 KP
    3. 按权重分配题数
    4. 从每个 KP 随机抽取指定数量
    """
    # 先获取学员加权掌握度
    weighted = calculate_weighted_mastery(db, student_id, syllabus_target)
    mastery_map: Dict[str, str] = {
        r.knowledge_point: r.mastery_level for r in weighted
    }

    # 获取该 syllabus 下所有有题的 KP
    all_kps_db = (
        db.query(Question.knowledge_point)
        .filter(Question.syllabus_version == syllabus_target)
        .distinct()
        .all()
    )
    all_kps = [kp for (kp,) in all_kps_db]
    if not all_kps:
        return []

    # 构建权重表
    kp_weights: Dict[str, Decimal] = {}
    for kp in all_kps:
        level = mastery_map.get(kp, "unknown")
        weight = WEIGHTS.get(level, WEIGHTS["unknown"])
        kp_weights[kp] = weight

    # 查各 KP 可用题数
    kp_avail = _kp_question_counts(db, syllabus_target, all_kps)

    # 分配题数
    allocations = _allocate_counts(count, kp_weights, kp_avail)

    # 按分配从各 KP 随机抽题
    result: List[Question] = []
    for alloc in allocations:
        if alloc.allocated <= 0:
            continue
        qs = (
            db.query(Question)
            .filter(Question.syllabus_version == syllabus_target)
            .filter(Question.knowledge_point == alloc.knowledge_point)
            .order_by(sa_func.random())
            .limit(alloc.allocated)
            .all()
        )
        result.extend(qs)

    return result


def get_allocation_preview(
    db: Session,
    student_id: int,
    syllabus_target: str,
    count: int,
) -> List[KpAllocation]:
    """预览抽题分配（用于调试/老师端查看）。"""
    weighted = calculate_weighted_mastery(db, student_id, syllabus_target)
    mastery_map: Dict[str, str] = {
        r.knowledge_point: r.mastery_level for r in weighted
    }

    all_kps_db = (
        db.query(Question.knowledge_point)
        .filter(Question.syllabus_version == syllabus_target)
        .distinct()
        .all()
    )
    all_kps = [kp for (kp,) in all_kps_db]
    if not all_kps:
        return []

    kp_weights: Dict[str, Decimal] = {}
    for kp in all_kps:
        level = mastery_map.get(kp, "unknown")
        weight = WEIGHTS.get(level, WEIGHTS["unknown"])
        kp_weights[kp] = weight

    kp_avail = _kp_question_counts(db, syllabus_target, all_kps)
    allocations = _allocate_counts(count, kp_weights, kp_avail)

    # 补充 mastery_level 信息
    for alloc in allocations:
        alloc.mastery_level = mastery_map.get(alloc.knowledge_point, "unknown")

    return sorted(allocations, key=lambda x: x.weight, reverse=True)
