"""题库相关 schemas。"""
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field

QType = Literal["single", "judge", "coding", "program"]
ProgramLang = Literal["scratch", "python", "cpp"]


class QuestionBase(BaseModel):
    syllabus_version: str = Field(..., max_length=32)
    grade_level: int = Field(..., ge=1, le=12)
    knowledge_point: str = Field(..., max_length=128)
    q_type: QType
    content: str
    difficulty: int = Field(default=1, ge=1, le=5)
    explanation: Optional[str] = None
    blocks_json: Optional[str] = None
    grading_rules: Optional[str] = None
    program_lang: Optional[ProgramLang] = None


class QuestionOut(QuestionBase):
    """老师端/管理端：含 answer（完整数据）"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    answer: str
    created_at: datetime

    @computed_field
    @property
    def blocks(self) -> Optional[List[str]]:
        if not self.blocks_json:
            return None
        import json
        try:
            return json.loads(self.blocks_json)
        except (ValueError, TypeError):
            return None

    @computed_field
    @property
    def grading_rules_parsed(self) -> Optional[Any]:
        if not self.grading_rules:
            return None
        import json
        try:
            return json.loads(self.grading_rules)
        except (ValueError, TypeError):
            return None


class QuestionOutStudent(QuestionBase):
    """学员端：隐藏 answer，仅含 blocks 供拼积木题展示 + grading_rules 供编程题判题"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

    @computed_field
    @property
    def blocks(self) -> Optional[List[str]]:
        if not self.blocks_json:
            return None
        import json
        try:
            return json.loads(self.blocks_json)
        except (ValueError, TypeError):
            return None

    @computed_field
    @property
    def grading_rules_parsed(self) -> Optional[Any]:
        """编程大题的判题规则（学员端需要知道检查哪些积木/测试用例）"""
        if not self.grading_rules:
            return None
        import json
        try:
            rules = json.loads(self.grading_rules)
            # 对 python/cpp 题，隐藏 expected 字段防止作弊
            if isinstance(rules, dict) and "test_cases" in rules:
                safe_cases = []
                for tc in rules.get("test_cases", []):
                    safe_cases.append({"input": tc.get("input", ""), "hint": tc.get("hint", "")})
                return {
                    "language": rules.get("language"),
                    "time_limit": rules.get("time_limit", 2),
                    "memory_limit": rules.get("memory_limit", 128),
                    "test_case_count": len(rules.get("test_cases", [])),
                    "test_cases": safe_cases,
                }
            # scratch 题的规则不泄露答案，只返回规则数量
            if isinstance(rules, list):
                return {"check_count": len(rules)}
            return rules
        except (ValueError, TypeError):
            return None


class QuestionListResp(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[QuestionOut]


class QuestionFilter(BaseModel):
    syllabus_version: Optional[str] = None
    grade_level: Optional[int] = None
    q_type: Optional[QType] = None
