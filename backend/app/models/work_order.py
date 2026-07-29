"""补课工单表模型。"""
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


class WorkOrder(Base):
    """补课工单：老师针对学员薄弱知识点推送的补课任务。"""

    __tablename__ = "work_orders"

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    student_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    # 关联的诊断会话 ID（可选，手动创建的工单可能没有）
    session_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("diagnosis_sessions.id", ondelete="SET NULL"), nullable=True
    )
    # 创建工单的老师 ID
    teacher_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True
    )
    # 被分配处理工单的老师 ID（教学主管可指派给普通教师）
    assignee_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True
    )
    syllabus_target: Mapped[str] = mapped_column(String(32), nullable=False)
    # 薄弱知识点，多个用英文逗号分隔
    weak_kps: Mapped[str] = mapped_column(Text, nullable=False)
    # 工单标题
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    # 补课说明 / 建议
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # 关联的奇码课件章节，JSON 数组
    chapters_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    # 状态：pending / in_progress / completed / cancelled
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="pending", server_default="pending"
    )
    # 优先级：low / medium / high
    priority: Mapped[str] = mapped_column(
        String(16), nullable=False, default="medium", server_default="medium"
    )
    # 截止日期
    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
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
        Index("ix_wo_student_id", "student_id"),
        Index("ix_wo_status", "status"),
        Index("ix_wo_created_at", "created_at"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<WorkOrder id={self.id} student={self.student_id} status={self.status}>"
