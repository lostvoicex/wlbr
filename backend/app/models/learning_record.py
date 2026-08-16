"""学习记录表模型。"""
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class LearningRecord(Base):
    """学习记录：一次学员对某道题的作答留痕。"""

    __tablename__ = "learning_records"

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    student_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("students.id", ondelete="SET NULL"), nullable=True
    )
    question_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("questions.id", ondelete="SET NULL"), nullable=True
    )
    student_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_correct: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    # 会话类型：diagnosis / retest_t1 / retest_t2（与 DiagnosisSession.session_type 对齐）
    session_type: Mapped[str | None] = mapped_column(String(16), nullable=True)
    session_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    # 反作弊：作答耗时（秒），前端上报
    answer_duration_sec: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # 反作弊：作答时长是否可疑（过快/过慢）
    duration_suspicious: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("ix_lr_student_session", "student_id", "session_type"),
        Index("ix_lr_question", "question_id"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<LearningRecord id={self.id} student={self.student_id} q={self.question_id}>"
