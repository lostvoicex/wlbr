"""映射审核记录表模型。"""
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class MappingReview(Base):
    """映射审核记录：每次一审/二审操作留痕。"""

    __tablename__ = "mapping_reviews"

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    mapping_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("kp_mappings.id", ondelete="CASCADE"), nullable=False
    )
    # 审核人
    reviewer_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True
    )
    # 第几审：1 / 2
    review_round: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    # 审核结果：approved / rejected / needs_review
    result: Mapped[str] = mapped_column(String(16), nullable=False)
    # 审核后映射的等级 1-5
    review_level: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    # 审核备注
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("ix_mr_mapping_id", "mapping_id"),
        Index("ix_mr_reviewer_id", "reviewer_id"),
        Index("ix_mr_created_at", "created_at"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<MappingReview id={self.id} mapping={self.mapping_id} round={self.review_round}>"
