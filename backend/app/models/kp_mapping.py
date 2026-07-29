"""KP 映射表模型：知识点 → 奇码课件章节映射。"""
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


class KpMapping(Base):
    """知识点 → 奇码课件章节映射关系。

    每个 KP 可以映射到多个课件章节，每个映射需要经过二审流程。
    """

    __tablename__ = "kp_mappings"

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    syllabus_version: Mapped[str] = mapped_column(String(32), nullable=False)
    knowledge_point: Mapped[str] = mapped_column(String(128), nullable=False)
    # 课件名称 / 教材名
    courseware_name: Mapped[str] = mapped_column(String(255), nullable=False)
    # 章节号，如 "第3章" 或 "L1-Unit3"
    chapter: Mapped[str] = mapped_column(String(64), nullable=False)
    # 页码或具体位置描述
    page_ref: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # 章节标题 / 知识点在课件中的名称
    chapter_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # 匹配度 0-100，AI 自动映射时使用
    match_score: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, default=0, server_default="0"
    )
    # 映射来源：ai / manual / import
    source: Mapped[str] = mapped_column(
        String(16), nullable=False, default="manual", server_default="manual"
    )
    # 审核状态：pending / approved / rejected / needs_review
    review_status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="pending", server_default="pending"
    )
    # 当前审核等级 1-5（5 档二审枚举）
    review_level: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, default=1, server_default="1"
    )
    # 一审人
    reviewer1_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True
    )
    # 二审人
    reviewer2_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True
    )
    # 审核备注
    review_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    # 是否启用（停用后不展示在学员端）
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    # 排序权重
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        Index("ix_kpm_syllabus_kp", "syllabus_version", "knowledge_point"),
        Index("ix_kpm_review_status", "review_status"),
        Index("ix_kpm_courseware", "courseware_name"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<KpMapping id={self.id} kp={self.knowledge_point} chapter={self.chapter}>"
