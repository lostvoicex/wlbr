"""OJ 编程题提交相关 schemas。"""
from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class OjSubmitRequest(BaseModel):
    """学员提交编程大题。"""
    question_id: int = Field(..., description="题目 ID")
    session_id: Optional[int] = Field(None, description="诊断会话 ID（诊断中提交时传入）")
    language: str = Field(..., pattern=r"^(scratch|python|cpp)$", description="提交语言")
    code: str = Field(..., description="提交内容：scratch→sb3的base64 / python|cpp→源代码")


class OjTestCaseResult(BaseModel):
    """单个测试用例结果。"""
    input: str
    expected: str
    actual: Optional[str] = None
    passed: bool
    msg: Optional[str] = None


class OjRuleResult(BaseModel):
    """Scratch 单条判题规则结果。"""
    rule: str
    passed: bool
    desc: Optional[str] = None
    msg: Optional[str] = None


class OjSubmitResponse(BaseModel):
    """提交后返回的判题结果。"""
    model_config = ConfigDict(from_attributes=True)

    submission_id: int
    question_id: int
    language: str
    # verdict: accepted / wrong_answer / compile_error / runtime_error / time_limit / partial
    verdict: str
    score: int = Field(..., ge=0, le=100, description="得分 0-100")
    passed_cases: int = 0
    total_cases: int = 0
    # 详细反馈（规则详情或测试用例详情）
    details: Optional[Any] = None
    stderr: Optional[str] = None
    judge_duration_ms: Optional[int] = None
    created_at: datetime


class OjProblemInfo(BaseModel):
    """编程大题信息（学员端展示用）。"""
    id: int
    knowledge_point: str
    content: str
    program_lang: str
    grading_rules_parsed: Optional[Any] = None
