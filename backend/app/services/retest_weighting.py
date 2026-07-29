"""复测加权算法。

复测闭环：诊断 → T1（3天后）→ T2（7天后）
加权规则：
- 仅诊断：使用诊断结果
- 诊断 + T1：T1 权重 1.0（尚无 T2）
- 诊断 + T1 + T2：T1 × 0.3 + T2 × 0.7
- 诊断 + T2（跳过 T1）：T2 权重 1.0

加权后的掌握度仍然按 80/50 阈值分档。
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.models import DiagnosisSession, KpMasterySnapshot

MASTERED_THRESHOLD = Decimal("0.8")
REVIEW_THRESHOLD = Decimal("0.5")


@dataclass
class WeightedKpResult:
    knowledge_point: str
    correct_count: int
    total_count: int
    weighted_rate: Decimal
    mastery_level: str
    sources: List[str]  # 说明参与了哪些会话的计算


def _classify(rate: Decimal) -> str:
    if rate >= MASTERED_THRESHOLD:
        return "mastered"
    if rate >= REVIEW_THRESHOLD:
        return "need_review"
    return "need_repair"


def calculate_weighted_mastery(
    db: Session,
    student_id: int,
    syllabus_target: str,
) -> List[WeightedKpResult]:
    """计算学员在指定 syllabus 下每个 KP 的加权掌握度。

    查询该学员该 syllabus 下所有已完成会话的快照，
    按 KP 分组，取每个会话类型的最新一次，然后加权。
    """
    # 查询所有相关会话（已完成的）
    sessions: List[DiagnosisSession] = (
        db.query(DiagnosisSession)
        .filter(
            DiagnosisSession.student_id == student_id,
            DiagnosisSession.syllabus_target == syllabus_target,
            DiagnosisSession.status == "finished",
        )
        .order_by(DiagnosisSession.finished_at.asc())
        .all()
    )

    if not sessions:
        return []

    # 按 KP 分组收集各会话类型的最新快照
    # kp -> {session_type -> snapshot}
    kp_snapshots: Dict[str, Dict[str, KpMasterySnapshot]] = {}
    session_ids = [s.id for s in sessions]

    snaps: List[KpMasterySnapshot] = (
        db.query(KpMasterySnapshot)
        .filter(KpMasterySnapshot.session_id.in_(session_ids))
        .all()
    )

    # 建立 session_id -> session_type 映射
    session_type_map = {s.id: s.session_type for s in sessions}

    for snap in snaps:
        stype = session_type_map.get(snap.session_id, "diagnosis")
        kp = snap.knowledge_point
        if kp not in kp_snapshots:
            kp_snapshots[kp] = {}
        # 每个 session_type 只保留最新一条（按 created_at）
        existing = kp_snapshots[kp].get(stype)
        if existing is None or snap.created_at > existing.created_at:
            kp_snapshots[kp][stype] = snap

    results: List[WeightedKpResult] = []
    for kp, type_map in kp_snapshots.items():
        diagnosis_snap = type_map.get("diagnosis")
        t1_snap = type_map.get("retest_t1")
        t2_snap = type_map.get("retest_t2")

        weighted_rate = Decimal("0")
        total_count = 0
        correct_count = 0
        sources: List[str] = []

        if t2_snap is not None:
            # 有 T2，按 T1×0.3 + T2×0.7 加权
            if t1_snap is not None:
                # T1 + T2 加权
                weighted_rate = (
                    Decimal("0.3") * t1_snap.correct_rate
                    + Decimal("0.7") * t2_snap.correct_rate
                ).quantize(Decimal("0.0001"))
                # 总题数取 T2 的（复测通常题量固定）
                total_count = t2_snap.total_count
                correct_count = int(
                    round(float(weighted_rate) * total_count)
                )
                sources = ["retest_t1", "retest_t2"]
            else:
                # 只有 T2，权重 1.0
                weighted_rate = t2_snap.correct_rate
                total_count = t2_snap.total_count
                correct_count = t2_snap.correct_count
                sources = ["retest_t2"]
        elif t1_snap is not None:
            # 只有 T1，权重 1.0
            weighted_rate = t1_snap.correct_rate
            total_count = t1_snap.total_count
            correct_count = t1_snap.correct_count
            sources = ["retest_t1"]
        elif diagnosis_snap is not None:
            # 只有诊断
            weighted_rate = diagnosis_snap.correct_rate
            total_count = diagnosis_snap.total_count
            correct_count = diagnosis_snap.correct_count
            sources = ["diagnosis"]
        else:
            continue

        results.append(
            WeightedKpResult(
                knowledge_point=kp,
                correct_count=correct_count,
                total_count=total_count,
                weighted_rate=weighted_rate,
                mastery_level=_classify(weighted_rate),
                sources=sources,
            )
        )

    # 排序：需重点补 → 待巩固 → 已掌握
    order = {"need_repair": 0, "need_review": 1, "mastered": 2}
    results.sort(key=lambda x: (order.get(x.mastery_level, 9), -x.total_count))
    return results


def get_latest_mastery_for_kp(
    db: Session,
    student_id: int,
    syllabus_target: str,
    knowledge_point: str,
) -> Optional[WeightedKpResult]:
    """获取单个 KP 的最新加权掌握度。"""
    all_results = calculate_weighted_mastery(db, student_id, syllabus_target)
    for r in all_results:
        if r.knowledge_point == knowledge_point:
            return r
    return None
