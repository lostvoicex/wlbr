"""add learning_note column to students

Revision ID: 20250104_0004
Revises: 20250103_0003
Create Date: 2025-01-04 09:00:00
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20250104_0004"
down_revision: Union[str, None] = "20250103_0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """新增 `learning_note` 字段：学员学习备注（如 Scratch 水平：很棒 / 中等）。"""
    op.add_column(
        "students",
        sa.Column("learning_note", sa.String(length=50), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("students", "learning_note")
