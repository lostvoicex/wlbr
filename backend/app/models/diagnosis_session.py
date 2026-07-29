"""诊断会话表模型。"""
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class DiagnosisSession(Base):
    """诊断/复测会话：一次学员开始 → 结束的答题过程。"""

    __tablename__ = "diagnosis_sessions"

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    student_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    syllabus_target: Mapped[str] = mapped_column(String(32), nullable=False)
    # diagnosis / retest_t1 / retest_t2
    session_type: Mapped[str] = mapped_column(
        String(16), nullable=False, default="diagnosis", server_default="diagnosis"
    )
    total_count: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    correct_count: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, default=0, server_default="0"
    )
    # in_progress / finished / abandoned
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="in_progress", server_default="in_progress"
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # 反作弊：切屏次数
    tab_switch_count: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, default=0, server_default="0"
    )
    # 反作弊：是否可疑（切屏过多 / 答题时长异常等）
    suspicious_flag: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    # 反作弊：可疑原因（逗号分隔）
    suspicious_reason: Mapped[str | None] = mapped_column(
        String(256), nullable=True
    )

    __table_args__ = (Index("ix_ds_student_id", "student_id"),)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<DiagnosisSession id={self.id} student={self.student_id} status={self.status}>"
