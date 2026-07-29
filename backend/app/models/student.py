"""学员表模型。"""
from datetime import datetime

from sqlalchemy import BigInteger, CheckConstraint, DateTime, Index, Integer, SmallInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Student(Base):
    """学员：小学 2-6 年级少儿编程学员。"""

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    grade: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    # 密码哈希（学号+密码登录使用）；手机验证码登录时可留空
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    syllabus_target: Mapped[str | None] = mapped_column(String(32), nullable=True)
    # 学习备注（如 Scratch 水平：很棒 / 中等 / 起步中），供老师后台展示
    learning_note: Mapped[str | None] = mapped_column(String(50), nullable=True)
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
        CheckConstraint("grade BETWEEN 2 AND 6", name="ck_students_grade_range"),
        Index("ix_students_phone", "phone"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Student id={self.id} name={self.name} grade={self.grade}>"
