"""M1 初始迁移：students / questions / learning_records 三张核心表。

Revision ID: 20250101_0001
Revises:
Create Date: 2025-01-01 00:00:00
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20250101_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---------- students ----------
    op.create_table(
        "students",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("grade", sa.SmallInteger(), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("password_hash", sa.String(length=255), nullable=True),
        sa.Column("syllabus_target", sa.String(length=32), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint("grade BETWEEN 2 AND 6", name="ck_students_grade_range"),
        sa.UniqueConstraint("phone", name="uq_students_phone"),
    )
    op.create_index("ix_students_phone", "students", ["phone"], unique=False)

    # ---------- questions ----------
    op.create_table(
        "questions",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("syllabus_version", sa.String(length=32), nullable=False),
        sa.Column("grade_level", sa.SmallInteger(), nullable=False),
        sa.Column("knowledge_point", sa.String(length=128), nullable=False),
        sa.Column("q_type", sa.String(length=16), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("difficulty", sa.SmallInteger(), nullable=False, server_default="1"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "q_type IN ('single','judge','coding')", name="ck_questions_qtype_enum"
        ),
    )
    op.create_index(
        "ix_questions_syllabus_grade",
        "questions",
        ["syllabus_version", "grade_level"],
        unique=False,
    )
    op.create_index(
        "ix_questions_kp", "questions", ["knowledge_point"], unique=False
    )

    # ---------- learning_records ----------
    op.create_table(
        "learning_records",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("student_id", sa.BigInteger(), nullable=True),
        sa.Column("question_id", sa.BigInteger(), nullable=True),
        sa.Column("student_answer", sa.Text(), nullable=True),
        sa.Column("is_correct", sa.Boolean(), nullable=True),
        sa.Column("session_type", sa.String(length=16), nullable=True),
        sa.Column("session_id", sa.BigInteger(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["student_id"], ["students.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["question_id"], ["questions.id"], ondelete="SET NULL"
        ),
    )
    op.create_index(
        "ix_lr_student_session",
        "learning_records",
        ["student_id", "session_type"],
        unique=False,
    )
    op.create_index(
        "ix_lr_question", "learning_records", ["question_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_lr_question", table_name="learning_records")
    op.drop_index("ix_lr_student_session", table_name="learning_records")
    op.drop_table("learning_records")

    op.drop_index("ix_questions_kp", table_name="questions")
    op.drop_index("ix_questions_syllabus_grade", table_name="questions")
    op.drop_table("questions")

    op.drop_index("ix_students_phone", table_name="students")
    op.drop_table("students")
