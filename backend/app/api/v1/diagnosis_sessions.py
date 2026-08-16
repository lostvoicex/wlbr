"""诊断会话路由：/api/v1/diagnosis-sessions/*

核心闭环：
  POST /start              发起会话 → 抽 N 题（支持 diagnosis/retest_t1/retest_t2）
  POST /{id}/answer        逐题作答 → 写 learning_records，回增量正确数
  POST /{id}/finish        触发 KP 聚合 → 写 kp_mastery_snapshots
  GET  /{id}/result        结果报告数据（红/黄/绿三档 + 复测计划 + 课件章节）
  GET  /weighted-result    学员加权掌握度总览（T1×0.3 + T2×0.7）
"""
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session

from app.core.deps import CurrentUser, get_current_user
from app.db import get_db
from app.models import (
    DiagnosisSession,
    KpMapping,
    KpMasterySnapshot,
    LearningRecord,
    Question,
    Student,
    TabSwitchEvent,
    WorkOrder,
)
from app.schemas.diagnosis import (
    AnswerRequest,
    AnswerResponse,
    DiagnosisResultResponse,
    FinishDiagnosisResponse,
    PerKpResult,
    QuestionOutStudent,
    RetestPlan,
    StartDiagnosisRequest,
    StartDiagnosisResponse,
    TabSwitchRequest,
)
from app.services.mastery import aggregate_by_kp
from app.services.retest_weighting import calculate_weighted_mastery
from app.services.adaptive_selection import adaptive_select_questions

router = APIRouter(prefix="/diagnosis-sessions", tags=["diagnosis"])


def _require_student(user: CurrentUser) -> int:
    if user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="仅小朋友账号可以做闯关题"
        )
    try:
        return int(user.subject)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="账号信息异常"
        )


def _normalize(text: str) -> str:
    return (text or "").strip().replace("\u3000", " ").lower()


def _is_correct(question: Question, student_answer: str) -> bool:
    """M1 判分：
    - single：忽略大小写与空格
    - judge：接受 true/false/对/错/✅/❌ 等常见写法
    - coding（M1 简化为积木块排序）：与标准答案字符串完全一致
    """
    ans = _normalize(question.answer)
    stu = _normalize(student_answer)

    if question.q_type == "judge":
        truthy = {"true", "t", "1", "对", "正确", "是", "✅", "yes", "y"}
        falsy = {"false", "f", "0", "错", "错误", "否", "❌", "no", "n"}
        stu_flag = None
        if stu in truthy:
            stu_flag = True
        elif stu in falsy:
            stu_flag = False
        ans_flag = ans in truthy
        return stu_flag is not None and stu_flag == ans_flag

    return ans == stu


def _badge_of(rate: Decimal) -> str:
    if rate >= Decimal("0.8"):
        return "champion"
    if rate >= Decimal("0.5"):
        return "cheer"
    return "together"


# 反作弊阈值
DURATION_TOO_FAST_SEC = 3  # 答题小于 3 秒可疑
DURATION_TOO_SLOW_SEC = 300  # 答题大于 5 分钟可疑
TAB_SWITCH_SUSPICIOUS_THRESHOLD = 5  # 切屏超过 5 次标记可疑

# 标准诊断题型配比：15 选择 + 10 判断 + 2 编程 = 27 题
STANDARD_TYPE_COUNTS = {"single": 15, "judge": 10, "program": 2}
STANDARD_TOTAL = sum(STANDARD_TYPE_COUNTS.values())  # 27


def _calc_type_counts(total: int) -> Dict[str, int]:
    """根据总题数按 15:10:2 比例计算各题型数量。

    保证 program 至少 1 道（total >= 1 时），single 优先补齐余数。
    """
    if total <= 0:
        return {"single": 0, "judge": 0, "program": 0}
    if total == STANDARD_TOTAL:
        return dict(STANDARD_TYPE_COUNTS)

    # 按比例分配
    program = max(1, round(total * 2 / STANDARD_TOTAL)) if total >= 3 else 0
    judge = max(0, round(total * 10 / STANDARD_TOTAL))
    single = total - program - judge
    if single < 0:
        # 题太少，优先保证 single
        single = max(0, total - program)
        judge = total - program - single
    return {"single": single, "judge": judge, "program": program}


def _pick_by_type(
    db: Session,
    syllabus_target: str,
    type_counts: Dict[str, int],
) -> List[Question]:
    """按题型配比从题库中抽题，每个类型内随机抽取。"""
    result: List[Question] = []
    for q_type, count in type_counts.items():
        if count <= 0:
            continue
        qs = (
            db.query(Question)
            .filter(
                Question.syllabus_version == syllabus_target,
                Question.q_type == q_type,
            )
            .order_by(sa_func.random())
            .limit(count)
            .all()
        )
        result.extend(qs)
    # 按题型排序：单选 → 判断 → 积木排序 → 编程大题（编程题放最后）
    _type_order = {"single": 0, "judge": 1, "coding": 2, "program": 3}
    result.sort(key=lambda q: _type_order.get(q.q_type, 99))
    return result


def _check_duration_suspicious(duration: Optional[int]) -> bool:
    """判断作答时长是否可疑。"""
    if duration is None:
        return False
    return duration < DURATION_TOO_FAST_SEC or duration > DURATION_TOO_SLOW_SEC


def _update_suspicious_flag(db: Session, session: DiagnosisSession) -> None:
    """根据切屏次数和答题时长更新会话可疑标记。"""
    reasons: List[str] = []
    if session.tab_switch_count >= TAB_SWITCH_SUSPICIOUS_THRESHOLD:
        reasons.append(f"切屏{session.tab_switch_count}次")

    # 统计可疑答题记录数
    suspicious_count = (
        db.query(LearningRecord)
        .filter(LearningRecord.session_id == session.id)
        .filter(LearningRecord.duration_suspicious == True)
        .count()
    )
    if suspicious_count >= 3:
        reasons.append(f"{suspicious_count}题作答时长异常")

    if reasons:
        session.suspicious_flag = True
        session.suspicious_reason = ",".join(reasons)
    else:
        session.suspicious_flag = False
        session.suspicious_reason = None


def _build_retest_plan(finished_at: datetime) -> RetestPlan:
    """根据完成时间计算复测计划日期。"""
    # finished_at 可能是 UTC，转成本地日期（+8 时区）
    tz = timezone(timedelta(hours=8))
    if finished_at.tzinfo is None:
        finished_at = finished_at.replace(tzinfo=timezone.utc)
    local_dt = finished_at.astimezone(tz)

    t1 = local_dt.date() + timedelta(days=3)
    t2 = local_dt.date() + timedelta(days=7)

    return RetestPlan(
        t1_at=t1.isoformat(),
        t2_at=t2.isoformat(),
        t1_days=3,
        t2_days=7,
        t1_hint=f"{t1.month}月{t1.day}日 · 再来一小练",
        t2_hint=f"{t2.month}月{t2.day}日 · 再来一次大闯关",
    )


def _get_kp_ppt_refs(
    db: Session, syllabus_target: str, knowledge_points: List[str]
) -> Dict[str, str]:
    """查询 KP 关联的奇码课件章节，返回 {kp: '课件名 · 章节 · 页码'}。"""
    if not knowledge_points:
        return {}

    mappings: List[KpMapping] = (
        db.query(KpMapping)
        .filter(KpMapping.syllabus_version == syllabus_target)
        .filter(KpMapping.knowledge_point.in_(knowledge_points))
        .filter(KpMapping.is_active == True)
        .filter(KpMapping.review_status == "approved")
        .order_by(KpMapping.sort_order.asc())
        .all()
    )

    refs: Dict[str, str] = {}
    for m in mappings:
        kp = m.knowledge_point
        parts = [m.courseware_name, m.chapter]
        if m.page_ref:
            parts.append(f"P{m.page_ref}")
        refs[kp] = " · ".join(parts)
    return refs


def _pick_questions_for_retest(
    db: Session,
    student_id: int,
    syllabus_target: str,
    session_type: str,
    count: int,
) -> List[Question]:
    """复测抽题：只抽该学员薄弱 KP 相关的题目，同时保持 15:10:2 题型比例。

    从该学员该 syllabus 的加权结果中找出 need_review / need_repair 的 KP，
    按题型配比分配名额，再从薄弱 KP 池中均衡抽取。
    """
    weighted = calculate_weighted_mastery(db, student_id, syllabus_target)
    weak_kps = [r.knowledge_point for r in weighted if r.mastery_level in ("need_review", "need_repair")]

    # 计算各题型需要的数量
    type_counts = _calc_type_counts(count)

    if not weak_kps:
        # 没有薄弱 KP，按题型比例随机抽
        return _pick_by_type(db, syllabus_target, type_counts)

    # 构建薄弱 KP 的题库池，分题型
    kp_pool: Dict[str, List[Question]] = {}
    for kp in weak_kps:
        qs = (
            db.query(Question)
            .filter(Question.syllabus_version == syllabus_target)
            .filter(Question.knowledge_point == kp)
            .order_by(sa_func.random())
            .all()
        )
        if qs:
            kp_pool[kp] = qs

    picked: List[Question] = []

    # 按题型分别抽取，每个题型内按 KP 均衡
    for q_type, need in type_counts.items():
        if need <= 0:
            continue
        # 筛选该题型的题目
        type_pool: Dict[str, List[Question]] = {}
        for kp, qs in kp_pool.items():
            typed = [q for q in qs if q.q_type == q_type]
            if typed:
                type_pool[kp] = list(typed)

        remaining = need
        # 每个 KP 先取 1 道
        for kp, qs in type_pool.items():
            if remaining <= 0:
                break
            picked.append(qs[0])
            type_pool[kp] = qs[1:]
            remaining -= 1

        # 剩余名额循环补充
        while remaining > 0:
            added = False
            for kp, qs in list(type_pool.items()):
                if remaining <= 0:
                    break
                if qs:
                    picked.append(qs[0])
                    type_pool[kp] = qs[1:]
                    remaining -= 1
                    added = True
            if not added:
                # 薄弱 KP 该题型不够，从全库补
                extra = (
                    db.query(Question)
                    .filter(
                        Question.syllabus_version == syllabus_target,
                        Question.q_type == q_type,
                    )
                    .order_by(sa_func.random())
                    .limit(remaining)
                    .all()
                )
                picked.extend(extra)
                remaining -= len(extra)
                if not extra:
                    break

    # 打乱顺序
    import random
    random.shuffle(picked)
    return picked


# ---------------- Endpoints ----------------
@router.post(
    "/start",
    response_model=StartDiagnosisResponse,
    summary="开始一次诊断/复测闯关（抽题）",
)
def start(
    payload: StartDiagnosisRequest,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
) -> StartDiagnosisResponse:
    student_id = _require_student(user)
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="学员信息丢失，请重新登录"
        )

    # 检查是否有未完成的同类型会话
    existing = (
        db.query(DiagnosisSession)
        .filter(
            DiagnosisSession.student_id == student_id,
            DiagnosisSession.syllabus_target == payload.syllabus_target,
            DiagnosisSession.session_type == payload.session_type,
            DiagnosisSession.status == "in_progress",
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="你还有没完成的闯关，先做完这一次吧～",
        )

    # 抽题逻辑
    if payload.session_type in ("retest_t1", "retest_t2"):
        questions = _pick_questions_for_retest(
            db, student_id, payload.syllabus_target, payload.session_type, payload.count
        )
    else:
        # 诊断模式：先按 15:10:2 题型配比抽题
        type_counts = _calc_type_counts(payload.count)
        questions = _pick_by_type(db, payload.syllabus_target, type_counts)
        # 如果按题型抽题数量不足（题库不全），退化为随机抽题补齐
        if len(questions) < payload.count:
            existing_ids = {q.id for q in questions}
            extra_q = db.query(Question).filter(
                Question.syllabus_version == payload.syllabus_target
            )
            if existing_ids:
                extra_q = extra_q.filter(~Question.id.in_(existing_ids))
            extra = (
                extra_q.order_by(sa_func.random())
                .limit(payload.count - len(questions))
                .all()
            )
            questions.extend(extra)

    if not questions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="题库里还没有这个等级的题，先联系老师上传～",
        )

    session = DiagnosisSession(
        student_id=student_id,
        syllabus_target=payload.syllabus_target,
        session_type=payload.session_type,
        total_count=len(questions),
        correct_count=0,
        status="in_progress",
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return StartDiagnosisResponse(
        session_id=session.id,
        total_count=session.total_count,
        syllabus_target=session.syllabus_target,
        session_type=session.session_type,
        questions=[QuestionOutStudent.model_validate(q) for q in questions],
    )


@router.post(
    "/{session_id}/answer",
    response_model=AnswerResponse,
    summary="提交一道题的作答",
)
def submit_answer(
    session_id: int,
    payload: AnswerRequest,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
) -> AnswerResponse:
    student_id = _require_student(user)
    session = (
        db.query(DiagnosisSession)
        .filter(DiagnosisSession.id == session_id)
        .first()
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="闯关会话不存在"
        )
    if session.student_id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="这不是你的闯关"
        )
    if session.status != "in_progress":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="这次闯关已经结束啦"
        )

    question = (
        db.query(Question).filter(Question.id == payload.question_id).first()
    )
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="题目不存在"
        )

    correct = _is_correct(question, payload.student_answer)

    # 幂等：同 session 下同题只留一条记录（覆盖）
    existing = (
        db.query(LearningRecord)
        .filter(
            LearningRecord.session_id == session_id,
            LearningRecord.question_id == payload.question_id,
            LearningRecord.student_id == student_id,
        )
        .first()
    )
    prev_correct = bool(existing.is_correct) if existing else None

    duration_suspicious = _check_duration_suspicious(payload.answer_duration_sec)

    if existing:
        existing.student_answer = payload.student_answer
        existing.is_correct = correct
        existing.answer_duration_sec = payload.answer_duration_sec
        existing.duration_suspicious = duration_suspicious
    else:
        db.add(
            LearningRecord(
                student_id=student_id,
                question_id=payload.question_id,
                student_answer=payload.student_answer,
                is_correct=correct,
                session_type=session.session_type,
                session_id=session_id,
                answer_duration_sec=payload.answer_duration_sec,
                duration_suspicious=duration_suspicious,
            )
        )

    # 增量维护 correct_count
    if prev_correct is None:
        if correct:
            session.correct_count = (session.correct_count or 0) + 1
    else:
        if prev_correct and not correct:
            session.correct_count = max(0, (session.correct_count or 0) - 1)
        elif (not prev_correct) and correct:
            session.correct_count = (session.correct_count or 0) + 1

    # 反作弊：更新可疑标记
    _update_suspicious_flag(db, session)

    db.commit()
    db.refresh(session)

    return AnswerResponse(
        is_correct=correct,
        correct_count=session.correct_count,
        total_count=session.total_count,
    )


@router.post(
    "/{session_id}/tab-switch",
    summary="上报切屏事件（反作弊）",
)
def report_tab_switch(
    session_id: int,
    payload: TabSwitchRequest,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    """学员端页面切走/切回时上报，用于反作弊检测。"""
    student_id = _require_student(user)
    session = (
        db.query(DiagnosisSession)
        .filter(DiagnosisSession.id == session_id)
        .first()
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="闯关会话不存在"
        )
    if session.student_id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="这不是你的闯关"
        )
    if session.status != "in_progress":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="这次闯关已经结束啦"
        )

    # 记录事件
    event = TabSwitchEvent(
        student_id=student_id,
        session_id=session_id,
        event_type=payload.event_type,
        away_duration_sec=payload.away_duration_sec,
        page_info=payload.page_info,
    )
    db.add(event)

    # hide 事件计数（每切走一次算一次切屏）
    if payload.event_type == "hide":
        session.tab_switch_count = (session.tab_switch_count or 0) + 1
        _update_suspicious_flag(db, session)

    db.commit()
    return {"ok": True, "tab_switch_count": session.tab_switch_count}


@router.post(
    "/{session_id}/finish",
    response_model=FinishDiagnosisResponse,
    summary="完成闯关：触发 KP 聚合并生成快照",
)
def finish(
    session_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
) -> FinishDiagnosisResponse:
    student_id = _require_student(user)
    session = (
        db.query(DiagnosisSession)
        .filter(DiagnosisSession.id == session_id)
        .first()
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="闯关会话不存在"
        )
    if session.student_id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="这不是你的闯关"
        )

    # 聚合：只做一次；重复调用直接返回既有 result_url
    if session.status == "finished":
        rate = (
            Decimal(session.correct_count or 0)
            / Decimal(session.total_count)
            if session.total_count
            else Decimal("0")
        ).quantize(Decimal("0.0001"))
        return FinishDiagnosisResponse(
            session_id=session.id,
            result_url=f"/student/result/{session.id}",
            total_rate=float(rate),
        )

    rows = (
        db.query(Question.knowledge_point, LearningRecord.is_correct)
        .join(LearningRecord, LearningRecord.question_id == Question.id)
        .filter(
            LearningRecord.session_id == session_id,
            LearningRecord.student_id == student_id,
        )
        .all()
    )
    aggregates = aggregate_by_kp((kp, ok) for kp, ok in rows)

    # 清掉旧快照（幂等重跑保护）
    db.query(KpMasterySnapshot).filter(
        KpMasterySnapshot.session_id == session_id
    ).delete(synchronize_session=False)

    for agg in aggregates:
        db.add(
            KpMasterySnapshot(
                student_id=student_id,
                session_id=session_id,
                knowledge_point=agg.knowledge_point,
                correct_count=agg.correct_count,
                total_count=agg.total_count,
                correct_rate=agg.correct_rate,
                mastery_level=agg.mastery_level,
            )
        )

    session.status = "finished"
    session.finished_at = datetime.now(tz=timezone.utc)
    db.commit()
    db.refresh(session)

    rate = (
        Decimal(session.correct_count or 0) / Decimal(session.total_count)
        if session.total_count
        else Decimal("0")
    ).quantize(Decimal("0.0001"))

    return FinishDiagnosisResponse(
        session_id=session.id,
        result_url=f"/student/result/{session.id}",
        total_rate=float(rate),
    )


@router.get(
    "/{session_id}/result",
    response_model=DiagnosisResultResponse,
    summary="获取结果报告数据",
)
def get_result(
    session_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
) -> DiagnosisResultResponse:
    student_id = _require_student(user)
    session = (
        db.query(DiagnosisSession)
        .filter(DiagnosisSession.id == session_id)
        .first()
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="闯关会话不存在"
        )
    if session.student_id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="这不是你的闯关"
        )

    snapshots: List[KpMasterySnapshot] = (
        db.query(KpMasterySnapshot)
        .filter(KpMasterySnapshot.session_id == session_id)
        .all()
    )
    # 按 need_repair -> need_review -> mastered 排序
    order = {"need_repair": 0, "need_review": 1, "mastered": 2}
    snapshots.sort(
        key=lambda s: (order.get(s.mastery_level, 9), -s.total_count)
    )

    # 查询 KP 关联的课件章节
    kps = [s.knowledge_point for s in snapshots]
    ppt_refs = _get_kp_ppt_refs(db, session.syllabus_target, kps)

    per_kp = [
        PerKpResult(
            knowledge_point=s.knowledge_point,
            correct_count=s.correct_count,
            total_count=s.total_count,
            correct_rate=float(s.correct_rate),
            mastery_level=s.mastery_level,
            low_confidence=s.total_count <= 2,
            ppt_ref=ppt_refs.get(s.knowledge_point),
        )
        for s in snapshots
    ]

    total_rate = (
        Decimal(session.correct_count or 0) / Decimal(session.total_count)
        if session.total_count
        else Decimal("0")
    ).quantize(Decimal("0.0001"))

    # 计算复测计划
    retest_plan = RetestPlan()
    if session.finished_at:
        retest_plan = _build_retest_plan(session.finished_at)

    return DiagnosisResultResponse(
        session_id=session.id,
        student_id=session.student_id,
        syllabus_target=session.syllabus_target,
        session_type=session.session_type,
        total_count=session.total_count,
        correct_count=session.correct_count or 0,
        total_rate=float(total_rate),
        badge=_badge_of(total_rate),
        started_at=session.started_at,
        finished_at=session.finished_at,
        per_kp=per_kp,
        retest_plan=retest_plan,
    )


@router.get(
    "/weighted-result",
    summary="学员加权掌握度总览（T1×0.3 + T2×0.7）",
)
def get_weighted_result(
    syllabus_target: str = Query(..., description="如 scratch-l1"),
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    """返回学员在指定 syllabus 下每个 KP 的加权掌握度。"""
    student_id = _require_student(user)
    results = calculate_weighted_mastery(db, student_id, syllabus_target)

    # 查询课件章节
    kps = [r.knowledge_point for r in results]
    ppt_refs = _get_kp_ppt_refs(db, syllabus_target, kps)

    return {
        "student_id": student_id,
        "syllabus_target": syllabus_target,
        "total_kp": len(results),
        "items": [
            {
                "knowledge_point": r.knowledge_point,
                "correct_count": r.correct_count,
                "total_count": r.total_count,
                "weighted_rate": float(r.weighted_rate),
                "mastery_level": r.mastery_level,
                "sources": r.sources,
                "ppt_ref": ppt_refs.get(r.knowledge_point),
            }
            for r in results
        ],
    }


@router.post(
    "/{session_id}/share-to-teacher",
    summary="学员把诊断报告分享给老师（创建补课工单）",
)
def share_to_teacher(
    session_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    """学员完成诊断后，点击"分享给老师"，系统自动创建一个补课工单。

    工单的 assignee_id 为空（由教学主管后续分配），
    这样教学主管可以在工单池中看到待分配的学员报告。
    """
    student_id = _require_student(user)
    session = (
        db.query(DiagnosisSession)
        .filter(DiagnosisSession.id == session_id)
        .first()
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="闯关会话不存在"
        )
    if session.student_id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="这不是你的闯关"
        )
    if session.status != "finished":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="请先完成这次闯关"
        )

    # 检查是否已经分享过
    existing = (
        db.query(WorkOrder)
        .filter(WorkOrder.session_id == session_id)
        .first()
    )
    if existing:
        return {
            "ok": True,
            "work_order_id": existing.id,
            "message": "报告已经分享给老师啦",
        }

    # 获取快照中的薄弱知识点
    snapshots = (
        db.query(KpMasterySnapshot)
        .filter(KpMasterySnapshot.session_id == session_id)
        .all()
    )
    weak_kps = [
        s.knowledge_point
        for s in snapshots
        if s.mastery_level in ("need_repair", "need_review")
    ]

    # 获取学员信息
    student = db.query(Student).filter(Student.id == student_id).first()
    student_name = student.name if student else "未知学员"

    # 计算正确率
    total_rate = (
        Decimal(session.correct_count or 0) / Decimal(session.total_count)
        if session.total_count
        else Decimal("0")
    )
    rate_percent = int(total_rate * 100)

    # 创建工单
    work_order = WorkOrder(
        student_id=student_id,
        session_id=session_id,
        teacher_id=None,  # 学员发起的，没有创建老师
        assignee_id=None,  # 待教学主管分配
        syllabus_target=session.syllabus_target,
        weak_kps=",".join(weak_kps) if weak_kps else "",
        title=f"【学员分享】{student_name} 的{session.syllabus_target}诊断报告",
        description=f"学员主动分享了诊断报告。\n"
                    f"正确率：{rate_percent}%（{session.correct_count}/{session.total_count}）\n"
                    f"薄弱知识点：{len(weak_kps)} 个\n"
                    f"请教学主管分配处理老师。",
        status="pending",
        priority="medium",
    )
    db.add(work_order)
    db.commit()
    db.refresh(work_order)

    return {
        "ok": True,
        "work_order_id": work_order.id,
        "message": "报告已分享给老师，老师会尽快查看",
    }
