"""切屏事件表模型（反作弊）。"""
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class TabSwitchEvent(Base):
    """学员答题时的切屏/离开页面事件记录。"""

    __tablename__ = "tab_switch_events"

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
    # hide（切走）/ show（切回）
    event_type: Mapped[str] = mapped_column(String(16), nullable=False)
    # 切走后到切回时的时长（秒），仅 show 事件有
    away_duration_sec: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # 前端上报的页面路径 / 标题（调试用）
    page_info: Mapped[str | None] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (Index("ix_tse_session_id", "session_id"),)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<TabSwitchEvent id={self.id} session={self.session_id} type={self.event_type}>"
