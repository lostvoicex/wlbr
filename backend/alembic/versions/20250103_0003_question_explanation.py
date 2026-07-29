"""add explanation column to questions

Revision ID: 20250103_0003
Revises: 20250101_0002
Create Date: 2025-01-03 09:00:00
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20250103_0003"
down_revision: Union[str, None] = "20250101_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """新增 `explanation` 字段：童趣化解析文本，供结果报告页 & 老师二审展示。"""
    op.add_column(
        "questions",
        sa.Column("explanation", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("questions", "explanation")
