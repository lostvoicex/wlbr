"""OJ 提交记录表模型。"""
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


class OjSubmission(Base):
    """OJ 编程题提交记录。

    每次学员提交编程大题（Scratch sb3 / Python / C++ 代码）时创建一条记录，
    判题引擎异步判题后更新 verdict / score 等字段。
    """

    __tablename__ = "oj_submissions"

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    student_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
    )
    question_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
    )
    session_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("diagnosis_sessions.id", ondelete="SET NULL"),
        nullable=True,
    )
    # 提交语言：scratch / python / cpp
    language: Mapped[str] = mapped_column(String(16), nullable=False)
    # 提交内容：
    #   scratch → sb3 文件的 base64 编码
    #   python/cpp → 源代码文本
    code: Mapped[str] = mapped_column(Text, nullable=False)
    # 判题状态：pending / judging / accepted / wrong_answer / compile_error / runtime_error / time_limit / partial
    verdict: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending", server_default="pending"
    )
    # 得分 0-100
    score: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, default=0, server_default="0"
    )
    # 通过的测试用例数 / 总测试用例数（文本题用）
    passed_cases: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, default=0, server_default="0"
    )
    total_cases: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, default=0, server_default="0"
    )
    # 判题详细反馈（JSON 字符串）
    #   scratch → {"rules":[{"rule":"...","passed":true,"msg":"..."}], "details":"..."}
    #   python/cpp → {"cases":[{"input":"...","expected":"...","actual":"...","passed":true}], "compile_output":"..."}
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    # 编译器/运行时输出（错误信息等）
    stderr: Mapped[str | None] = mapped_column(Text, nullable=True)
    # 判题耗时（毫秒）
    judge_duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    judged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        Index("ix_oj_sub_student_q", "student_id", "question_id"),
        Index("ix_oj_sub_session", "session_id"),
        Index("ix_oj_sub_verdict", "verdict"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<OjSubmission id={self.id} student={self.student_id} q={self.question_id} verdict={self.verdict}>"
