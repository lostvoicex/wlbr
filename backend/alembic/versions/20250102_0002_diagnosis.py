"""M1 补齐：diagnosis_sessions / kp_mastery_snapshots

Revision ID: 20250101_0002
Revises: 20250101_0001
Create Date: 2025-01-02 00:00:00
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20250101_0002"
down_revision: Union[str, None] = "20250101_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---------- diagnosis_sessions ----------
    op.create_table(
        "diagnosis_sessions",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("student_id", sa.BigInteger(), nullable=False),
        sa.Column("syllabus_target", sa.String(length=32), nullable=False),
        sa.Column(
            "session_type",
            sa.String(length=16),
            nullable=False,
            server_default="diagnosis",
        ),
        sa.Column("total_count", sa.SmallInteger(), nullable=False),
        sa.Column(
            "correct_count", sa.SmallInteger(), nullable=False, server_default="0"
        ),
        sa.Column(
            "status",
            sa.String(length=16),
            nullable=False,
            server_default="in_progress",
        ),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["student_id"], ["students.id"], ondelete="CASCADE"
        ),
    )
    op.create_index(
        "ix_ds_student_id", "diagnosis_sessions", ["student_id"], unique=False
    )

    # ---------- kp_mastery_snapshots ----------
    op.create_table(
        "kp_mastery_snapshots",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("student_id", sa.BigInteger(), nullable=False),
        sa.Column("session_id", sa.BigInteger(), nullable=False),
        sa.Column("knowledge_point", sa.String(length=128), nullable=False),
        sa.Column("correct_count", sa.SmallInteger(), nullable=False),
        sa.Column("total_count", sa.SmallInteger(), nullable=False),
        sa.Column("correct_rate", sa.Numeric(5, 4), nullable=False),
        sa.Column("mastery_level", sa.String(length=16), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["student_id"], ["students.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["session_id"], ["diagnosis_sessions.id"], ondelete="CASCADE"
        ),
    )
    op.create_index(
        "ix_kp_session_id", "kp_mastery_snapshots", ["session_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_kp_session_id", table_name="kp_mastery_snapshots")
    op.drop_table("kp_mastery_snapshots")

    op.drop_index("ix_ds_student_id", table_name="diagnosis_sessions")
    op.drop_table("diagnosis_sessions")
