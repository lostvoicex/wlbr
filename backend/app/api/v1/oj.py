"""OJ 编程题路由：/api/v1/oj/*

编程大题判题闭环：
  GET  /problem/{question_id}   获取编程大题信息（含脱敏后的判题规则）
  POST /submit                  提交代码/作品 → 同步判题 → 返回结果
  GET  /submissions/{id}         查询某次提交结果
  GET  /submissions              学员提交历史列表
  GET  /history/{question_id}   学员在某题的历史提交

判题流程（同步）：
  1. 校验题目类型为 program，取出 grading_rules
  2. 根据 program_lang 分发到 sb3_grader / code_runner
  3. 写 OjSubmission 记录
  4. 若在诊断会话中（session_id 不为空），同步写/覆盖 LearningRecord（score>=60 视为通过）
     并维护 session.correct_count，确保 finish 时能正确做 KP 聚合
"""
import json
import time
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import CurrentUser, get_current_user
from app.db import get_db
from app.models import (
    DiagnosisSession,
    LearningRecord,
    OjSubmission,
    Question,
    Student,
)
from app.schemas.oj import (
    OjProblemInfo,
    OjSubmitRequest,
    OjSubmitResponse,
)
from app.services.code_runner import grade_code, grade_code_static
from app.services.sb3_grader import grade_sb3

router = APIRouter(prefix="/oj", tags=["oj"])

# 编程大题通过阈值：得分 >= 60 视为通过（写 LearningRecord.is_correct=True）
PROGRAM_PASS_THRESHOLD = 60


def _require_student(user: CurrentUser) -> int:
    if user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="只有小朋友账号可以提交编程大题"
        )
    try:
        return int(user.subject)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="账号信息异常"
        )


def _dispatch_grading(
    question: Question, code: str, language: str
) -> dict:
    """根据题目语言分发到对应判题引擎。

    Returns:
        判题引擎返回的标准化结果 dict。
    """
    rules_json = question.grading_rules or ""

    if language == "scratch":
        return grade_sb3(code, rules_json)

    if language in ("python", "cpp"):
        return grade_code(code, rules_json, language)

    return {
        "verdict": "compile_error",
        "score": 0,
        "passed_cases": 0,
        "total_cases": 0,
        "details": [],
        "stderr": f"不支持的语言: {language}",
    }


def _sync_to_learning_record(
    db: Session,
    student_id: int,
    question_id: int,
    session_id: int,
    session: DiagnosisSession,
    score: int,
    is_correct: bool,
) -> None:
    """把 OJ 判题结果同步到 LearningRecord，让 finish 时能做 KP 聚合。

    幂等：同 session 下同题只留一条记录（覆盖）。
    """
    existing = (
        db.query(LearningRecord)
        .filter(
            LearningRecord.session_id == session_id,
            LearningRecord.question_id == question_id,
            LearningRecord.student_id == student_id,
        )
        .first()
    )
    prev_correct = bool(existing.is_correct) if existing else None
    answer_summary = f"[OJ] score={score}"

    if existing:
        existing.student_answer = answer_summary
        existing.is_correct = is_correct
    else:
        db.add(
            LearningRecord(
                student_id=student_id,
                question_id=question_id,
                student_answer=answer_summary,
                is_correct=is_correct,
                session_type=session.session_type,
                session_id=session_id,
            )
        )

    # 增量维护 correct_count
    if prev_correct is None:
        if is_correct:
            session.correct_count = (session.correct_count or 0) + 1
    else:
        if prev_correct and not is_correct:
            session.correct_count = max(0, (session.correct_count or 0) - 1)
        elif (not prev_correct) and is_correct:
            session.correct_count = (session.correct_count or 0) + 1


# ---------------- Endpoints ----------------

@router.get(
    "/problem/{question_id}",
    response_model=OjProblemInfo,
    summary="获取编程大题信息（学员端展示用，判题规则已脱敏）",
)
def get_problem(
    question_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
) -> OjProblemInfo:
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="题目不存在")
    if q.q_type != "program":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="这不是编程大题"
        )
    if not q.program_lang:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="题目缺少编程语言配置"
        )

    # 复用 QuestionOutStudent 的脱敏逻辑
    from app.schemas.question import QuestionOutStudent
    q_out = QuestionOutStudent.model_validate(q)

    return OjProblemInfo(
        id=q.id,
        knowledge_point=q.knowledge_point,
        content=q.content,
        program_lang=q.program_lang,
        grading_rules_parsed=q_out.grading_rules_parsed,
    )


@router.post(
    "/submit",
    response_model=OjSubmitResponse,
    summary="提交编程大题并同步判题",
)
def submit(
    payload: OjSubmitRequest,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
) -> OjSubmitResponse:
    student_id = _require_student(user)
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="学员信息丢失，请重新登录"
        )

    question = db.query(Question).filter(Question.id == payload.question_id).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="题目不存在")
    if question.q_type != "program":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="这不是编程大题"
        )

    # 校验提交语言与题目配置一致
    if not question.program_lang:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="题目缺少编程语言配置"
        )
    if payload.language != question.program_lang:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"这道题要用 {question.program_lang} 来做哦",
        )

    # 校验会话
    session_obj: Optional[DiagnosisSession] = None
    if payload.session_id is not None:
        session_obj = (
            db.query(DiagnosisSession)
            .filter(DiagnosisSession.id == payload.session_id)
            .first()
        )
        if not session_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="闯关会话不存在"
            )
        if session_obj.student_id != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="这不是你的闯关"
            )
        if session_obj.status != "in_progress":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="这次闯关已经结束啦"
            )

    # 判题：优先执行代码（沙箱子进程模式），运行环境不可用时降级为静态分析
    start_ts = time.time()
    try:
        result = _dispatch_grading(question, payload.code, payload.language)
        stderr_str = result.get("stderr") or ""
        if result.get("score", 0) == 0 and "未找到" in stderr_str:
            rules_json = question.grading_rules or ""
            result = grade_code_static(payload.code, rules_json, payload.language)
    except Exception as e:
        rules_json = question.grading_rules or ""
        result = grade_code_static(payload.code, rules_json, payload.language)
        result["stderr"] = f"判题异常，已降级为静态分析: {e}"
    judge_duration_ms = int((time.time() - start_ts) * 1000)

    verdict = result.get("verdict", "wrong_answer")
    score = int(result.get("score", 0))
    passed_cases = int(result.get("passed_cases", result.get("passed_rules", 0)))
    total_cases = int(result.get("total_cases", result.get("total_rules", 0)))
    details = result.get("details", [])
    stderr_msg = result.get("stderr")

    # 写 OjSubmission
    submission = OjSubmission(
        student_id=student_id,
        question_id=payload.question_id,
        session_id=payload.session_id,
        language=payload.language,
        code=payload.code,
        verdict=verdict,
        score=score,
        passed_cases=passed_cases,
        total_cases=total_cases,
        feedback=json.dumps(details, ensure_ascii=False) if details else None,
        stderr=stderr_msg,
        judge_duration_ms=judge_duration_ms,
        judged_at=datetime.now(tz=timezone.utc),
    )
    db.add(submission)

    # 同步到 LearningRecord（诊断中）
    if session_obj is not None:
        is_correct = score >= PROGRAM_PASS_THRESHOLD
        _sync_to_learning_record(
            db,
            student_id,
            payload.question_id,
            payload.session_id,
            session_obj,
            score,
            is_correct,
        )

    db.commit()
    db.refresh(submission)

    return OjSubmitResponse(
        submission_id=submission.id,
        question_id=submission.question_id,
        language=submission.language,
        verdict=submission.verdict,
        score=submission.score,
        passed_cases=submission.passed_cases,
        total_cases=submission.total_cases,
        details=details,
        stderr=stderr_msg,
        judge_duration_ms=judge_duration_ms,
        created_at=submission.created_at,
    )


@router.get(
    "/submissions/{submission_id}",
    response_model=OjSubmitResponse,
    summary="查询某次提交结果",
)
def get_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
) -> OjSubmitResponse:
    student_id = _require_student(user)
    sub = db.query(OjSubmission).filter(OjSubmission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="提交记录不存在")
    if sub.student_id != student_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="这不是你的提交")

    details = None
    if sub.feedback:
        try:
            details = json.loads(sub.feedback)
        except (json.JSONDecodeError, TypeError):
            details = None

    return OjSubmitResponse(
        submission_id=sub.id,
        question_id=sub.question_id,
        language=sub.language,
        verdict=sub.verdict,
        score=sub.score,
        passed_cases=sub.passed_cases,
        total_cases=sub.total_cases,
        details=details,
        stderr=sub.stderr,
        judge_duration_ms=sub.judge_duration_ms,
        created_at=sub.created_at,
    )


@router.get(
    "/submissions",
    summary="学员提交历史列表",
)
def list_submissions(
    question_id: Optional[int] = Query(None, description="按题目过滤"),
    session_id: Optional[int] = Query(None, description="按会话过滤"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
) -> dict:
    student_id = _require_student(user)
    q = db.query(OjSubmission).filter(OjSubmission.student_id == student_id)
    if question_id is not None:
        q = q.filter(OjSubmission.question_id == question_id)
    if session_id is not None:
        q = q.filter(OjSubmission.session_id == session_id)

    total = q.count()
    items = (
        q.order_by(OjSubmission.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [
            {
                "submission_id": s.id,
                "question_id": s.question_id,
                "session_id": s.session_id,
                "language": s.language,
                "verdict": s.verdict,
                "score": s.score,
                "passed_cases": s.passed_cases,
                "total_cases": s.total_cases,
                "judge_duration_ms": s.judge_duration_ms,
                "created_at": s.created_at.isoformat() if s.created_at else None,
                "judged_at": s.judged_at.isoformat() if s.judged_at else None,
            }
            for s in items
        ],
    }


@router.get(
    "/history/{question_id}",
    summary="学员在某道编程题的历史提交",
)
def get_question_history(
    question_id: int,
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
) -> dict:
    student_id = _require_student(user)
    subs = (
        db.query(OjSubmission)
        .filter(
            OjSubmission.student_id == student_id,
            OjSubmission.question_id == question_id,
        )
        .order_by(OjSubmission.id.desc())
        .limit(limit)
        .all()
    )
    return {
        "question_id": question_id,
        "total": len(subs),
        "best_score": max((s.score for s in subs), default=0),
        "items": [
            {
                "submission_id": s.id,
                "language": s.language,
                "verdict": s.verdict,
                "score": s.score,
                "passed_cases": s.passed_cases,
                "total_cases": s.total_cases,
                "created_at": s.created_at.isoformat() if s.created_at else None,
            }
            for s in subs
        ],
    }
