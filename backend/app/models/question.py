"""题库表模型。"""
from datetime import datetime

from sqlalchemy import BigInteger, CheckConstraint, DateTime, Index, Integer, SmallInteger, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Question(Base):
    """题库：Scratch / Python 各级别诊断题。"""

    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    syllabus_version: Mapped[str] = mapped_column(String(32), nullable=False)
    grade_level: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    knowledge_point: Mapped[str] = mapped_column(String(128), nullable=False)
    # 题型：single(单选) / judge(判断) / coding(积木排序) / program(编程大题)
    q_type: Mapped[str] = mapped_column(String(16), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[int] = mapped_column(SmallInteger, default=1, nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    # coding 题（积木排序）的候选积木池，按答案顺序存 JSON 数组，前端负责 shuffle
    blocks_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    # program 题（编程大题）的判题规则，JSON 字符串：
    #   Scratch: [{"check":"opcode_exists","opcodes":["event_whenflagclicked"]}, ...]
    #   Python/C++: {"language":"python","test_cases":[{"input":"","expected":"Hello\\n"},{"input":"5","expected":"120\\n"}],"time_limit":2,"memory_limit":128}
    grading_rules: Mapped[str | None] = mapped_column(Text, nullable=True)
    # program 题的语言/编辑器类型：scratch / python / cpp
    program_lang: Mapped[str | None] = mapped_column(String(16), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "q_type IN ('single','judge','coding','program')",
            name="ck_questions_qtype_enum",
        ),
        CheckConstraint(
            "program_lang IN ('scratch','python','cpp') OR program_lang IS NULL",
            name="ck_questions_program_lang_enum",
        ),
        Index("ix_questions_syllabus_grade", "syllabus_version", "grade_level"),
        Index("ix_questions_kp", "knowledge_point"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Question id={self.id} kp={self.knowledge_point} type={self.q_type}>"
