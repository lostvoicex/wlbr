"""add blocks_json column to questions (coding 题积木池 JSON 存储)

Revision ID: 20250105_0005
Revises: 20250104_0004
Create Date: 2025-01-05 09:00:00
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20250105_0005"
down_revision: Union[str, None] = "20250104_0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """新增 `blocks_json` 字段：coding 题的候选积木池（按答案顺序存 JSON 数组）。"""
    op.add_column(
        "questions",
        sa.Column("blocks_json", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("questions", "blocks_json")
