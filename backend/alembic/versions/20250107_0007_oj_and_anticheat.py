"""第七批迁移：OJ 编程题 + 反作弊字段补全。

包含：
  1. questions 新增 grading_rules / program_lang 字段 + 更新 q_type 约束（加 program）
  2. diagnosis_sessions 新增 tab_switch_count / suspicious_flag / suspicious_reason
  3. learning_records 新增 answer_duration_sec / duration_suspicious
  4. 新建 tab_switch_events 表
  5. 新建 oj_submissions 表

Revision ID: 0007_oj_anticheat
Revises: 0006_m2_tables
Create Date: 2025-01-07 00:00:00.000000
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0007_oj_anticheat"
down_revision: Union[str, None] = "0006_m2_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---------- 1. questions 新增字段 ----------
    op.add_column(
        "questions",
        sa.Column("grading_rules", sa.Text(), nullable=True),
    )
    op.add_column(
        "questions",
        sa.Column("program_lang", sa.String(length=16), nullable=True),
    )
    # 更新 q_type 约束：加入 program
    op.drop_constraint("ck_questions_qtype_enum", "questions", type_="check")
    op.create_check_constraint(
        "ck_questions_qtype_enum",
        "questions",
        "q_type IN ('single','judge','coding','program')",
    )
    op.create_check_constraint(
        "ck_questions_program_lang_enum",
        "questions",
        "program_lang IN ('scratch','python','cpp') OR program_lang IS NULL",
    )

    # ---------- 2. diagnosis_sessions 新增反作弊字段 ----------
    op.add_column(
        "diagnosis_sessions",
        sa.Column(
            "tab_switch_count",
            sa.SmallInteger(),
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "diagnosis_sessions",
        sa.Column(
            "suspicious_flag",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column(
        "diagnosis_sessions",
        sa.Column("suspicious_reason", sa.String(length=256), nullable=True),
    )

    # ---------- 3. learning_records 新增反作弊字段 ----------
    op.add_column(
        "learning_records",
        sa.Column("answer_duration_sec", sa.Integer(), nullable=True),
    )
    op.add_column(
        "learning_records",
        sa.Column(
            "duration_suspicious",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )

    # ---------- 4. tab_switch_events 表 ----------
    op.create_table(
        "tab_switch_events",
        sa.Column(
            "id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            primary_key=True,
            autoincrement=True,
        ),
        sa.Column(
            "student_id",
            sa.BigInteger(),
            sa.ForeignKey("students.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "session_id",
            sa.BigInteger(),
            sa.ForeignKey("diagnosis_sessions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("event_type", sa.String(length=16), nullable=False),
        sa.Column("away_duration_sec", sa.Integer(), nullable=True),
        sa.Column("page_info", sa.String(length=256), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_tse_session_id", "tab_switch_events", ["session_id"])

    # ---------- 5. oj_submissions 表 ----------
    op.create_table(
        "oj_submissions",
        sa.Column(
            "id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            primary_key=True,
            autoincrement=True,
        ),
        sa.Column(
            "student_id",
            sa.BigInteger(),
            sa.ForeignKey("students.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "question_id",
            sa.BigInteger(),
            sa.ForeignKey("questions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "session_id",
            sa.BigInteger(),
            sa.ForeignKey("diagnosis_sessions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("language", sa.String(length=16), nullable=False),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column(
            "verdict",
            sa.String(length=20),
            nullable=False,
            server_default="pending",
        ),
        sa.Column(
            "score", sa.SmallInteger(), nullable=False, server_default="0"
        ),
        sa.Column(
            "passed_cases", sa.SmallInteger(), nullable=False, server_default="0"
        ),
        sa.Column(
            "total_cases", sa.SmallInteger(), nullable=False, server_default="0"
        ),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("stderr", sa.Text(), nullable=True),
        sa.Column("judge_duration_ms", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("judged_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_oj_sub_student_q", "oj_submissions", ["student_id", "question_id"]
    )
    op.create_index("ix_oj_sub_session", "oj_submissions", ["session_id"])
    op.create_index("ix_oj_sub_verdict", "oj_submissions", ["verdict"])


def downgrade() -> None:
    # oj_submissions
    op.drop_index("ix_oj_sub_verdict", table_name="oj_submissions")
    op.drop_index("ix_oj_sub_session", table_name="oj_submissions")
    op.drop_index("ix_oj_sub_student_q", table_name="oj_submissions")
    op.drop_table("oj_submissions")

    # tab_switch_events
    op.drop_index("ix_tse_session_id", table_name="tab_switch_events")
    op.drop_table("tab_switch_events")

    # learning_records
    op.drop_column("learning_records", "duration_suspicious")
    op.drop_column("learning_records", "answer_duration_sec")

    # diagnosis_sessions
    op.drop_column("diagnosis_sessions", "suspicious_reason")
    op.drop_column("diagnosis_sessions", "suspicious_flag")
    op.drop_column("diagnosis_sessions", "tab_switch_count")

    # questions
    op.drop_constraint("ck_questions_program_lang_enum", "questions", type_="check")
    op.drop_constraint("ck_questions_qtype_enum", "questions", type_="check")
    op.create_check_constraint(
        "ck_questions_qtype_enum",
        "questions",
        "q_type IN ('single','judge','coding')",
    )
    op.drop_column("questions", "program_lang")
    op.drop_column("questions", "grading_rules")
