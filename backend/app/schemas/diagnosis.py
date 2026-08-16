from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.question import QuestionOutStudent


class StartDiagnosisRequest(BaseModel):
    syllabus_target: str = Field(..., description="诊断目标，如 scratch-l1 / scratch-l2")
    count: int = Field(default=10, ge=1, le=30, description="抽题数量")
    session_type: str = Field(
        default="diagnosis",
        pattern=r"^(diagnosis|retest_t1|retest_t2)$",
        description="会话类型：诊断 / 复测T1 / 复测T2",
    )


class StartDiagnosisResponse(BaseModel):
    session_id: int
    total_count: int
    syllabus_target: str
    session_type: str
    questions: List[QuestionOutStudent]


class AnswerRequest(BaseModel):
    question_id: int
    student_answer: str = Field(..., description="学员提交的答案（coding 题用 → 拼接）")
    answer_duration_sec: Optional[int] = Field(
        None, ge=0, le=3600, description="作答耗时（秒），前端上报用于反作弊"
    )


class AnswerResponse(BaseModel):
    is_correct: bool
    correct_count: int
    total_count: int


class TabSwitchRequest(BaseModel):
    event_type: str = Field(..., pattern=r"^(hide|show)$", description="切走/切回")
    away_duration_sec: Optional[int] = Field(
        None, ge=0, le=3600, description="离开时长（秒），仅 show 事件上报"
    )
    page_info: Optional[str] = Field(None, max_length=256, description="页面信息（调试用）")


class FinishDiagnosisResponse(BaseModel):
    session_id: int
    result_url: str
    total_rate: float


class PerKpResult(BaseModel):
    knowledge_point: str
    correct_count: int
    total_count: int
    correct_rate: float
    mastery_level: str
    low_confidence: bool = False
    ppt_ref: Optional[str] = None  # 关联的奇码课件章节


class RetestPlan(BaseModel):
    t1_at: Optional[str] = None  # ISO 格式日期，如 "2026-07-27"
    t2_at: Optional[str] = None  # ISO 格式日期，如 "2026-07-31"
    t1_days: int = 3
    t2_days: int = 7
    t1_hint: str = "3 天后再来一小练"
    t2_hint: str = "7 天后再来一次大闯关"


class DiagnosisResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_id: int
    student_id: int
    syllabus_target: str
    session_type: str
    total_count: int
    correct_count: int
    total_rate: float
    badge: str
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    per_kp: List[PerKpResult]
    retest_plan: RetestPlan


class AnswerDetailItem(BaseModel):
    """单道题的答题明细。"""
    question_id: int
    q_type: str
    knowledge_point: str
    content: str
    student_answer: Optional[str] = None
    correct_answer: str
    is_correct: Optional[bool] = None
    explanation: Optional[str] = None
    program_lang: Optional[str] = None


class SessionAnswersResponse(BaseModel):
    """会话答题明细（错题列表）。"""
    session_id: int
    student_id: int
    student_name: str
    session_type: str
    syllabus_target: str
    total_count: int
    correct_count: int
    items: List[AnswerDetailItem]
