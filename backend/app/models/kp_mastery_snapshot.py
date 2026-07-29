"""KP 掌握度快照表模型。"""
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    SmallInteger,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class KpMasterySnapshot(Base):
    """一次会话结束后，对每个知识点的掌握度快照。"""

    __tablename__ = "kp_mastery_snapshots"

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    student_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    session_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("diagnosis_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    knowledge_point: Mapped[str] = mapped_column(String(128), nullable=False)
    correct_count: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    total_count: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    correct_rate: Mapped[Decimal] = mapped_column(Numeric(5, 4), nullable=False)
    # mastered / need_review / need_repair
    mastery_level: Mapped[str] = mapped_column(String(16), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (Index("ix_kp_session_id", "session_id"),)

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<KpMasterySnapshot id={self.id} kp={self.knowledge_point}"
            f" level={self.mastery_level}>"
        )
