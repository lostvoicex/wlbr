"""老师表模型。"""
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Index, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Teacher(Base):
    """老师/管理员账号。"""

    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    # 工号，如 T001 / admin
    teacher_no: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    # teacher / admin
    role: Mapped[str] = mapped_column(
        String(16), nullable=False, default="teacher", server_default="teacher"
    )
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(128), nullable=True)
    # 状态：active / disabled
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="active", server_default="active"
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
        Index("ix_teachers_teacher_no", "teacher_no", unique=True),
        Index("ix_teachers_role", "role"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Teacher id={self.id} no={self.teacher_no} name={self.name}>"
