"""第六批迁移：新增 teachers / work_orders / kp_mappings / mapping_reviews 四张表。

Revision ID: 0006_m2_tables
Revises: 20250105_0005
Create Date: 2025-01-06 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0006_m2_tables"
down_revision = "20250105_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # teachers 表
    op.create_table(
        "teachers",
        sa.Column("id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), primary_key=True, autoincrement=True),
        sa.Column("teacher_no", sa.String(32), nullable=False, unique=True),
        sa.Column("name", sa.String(64), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(16), nullable=False, server_default="teacher"),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("email", sa.String(128), nullable=True),
        sa.Column("status", sa.String(16), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_teachers_teacher_no", "teachers", ["teacher_no"], unique=True)
    op.create_index("ix_teachers_role", "teachers", ["role"])

    # work_orders 表
    op.create_table(
        "work_orders",
        sa.Column("id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), primary_key=True, autoincrement=True),
        sa.Column("student_id", sa.BigInteger(), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("session_id", sa.BigInteger(), sa.ForeignKey("diagnosis_sessions.id", ondelete="SET NULL"), nullable=True),
        sa.Column("teacher_id", sa.BigInteger(), sa.ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True),
        sa.Column("syllabus_target", sa.String(32), nullable=False),
        sa.Column("weak_kps", sa.Text(), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("chapters_json", sa.Text(), nullable=True),
        sa.Column("status", sa.String(16), nullable=False, server_default="pending"),
        sa.Column("priority", sa.String(16), nullable=False, server_default="medium"),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_wo_student_id", "work_orders", ["student_id"])
    op.create_index("ix_wo_status", "work_orders", ["status"])
    op.create_index("ix_wo_created_at", "work_orders", ["created_at"])

    # kp_mappings 表
    op.create_table(
        "kp_mappings",
        sa.Column("id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), primary_key=True, autoincrement=True),
        sa.Column("syllabus_version", sa.String(32), nullable=False),
        sa.Column("knowledge_point", sa.String(128), nullable=False),
        sa.Column("courseware_name", sa.String(255), nullable=False),
        sa.Column("chapter", sa.String(64), nullable=False),
        sa.Column("page_ref", sa.String(64), nullable=True),
        sa.Column("chapter_title", sa.String(255), nullable=True),
        sa.Column("match_score", sa.SmallInteger(), nullable=False, server_default="0"),
        sa.Column("source", sa.String(16), nullable=False, server_default="manual"),
        sa.Column("review_status", sa.String(16), nullable=False, server_default="pending"),
        sa.Column("review_level", sa.SmallInteger(), nullable=False, server_default="1"),
        sa.Column("reviewer1_id", sa.BigInteger(), sa.ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True),
        sa.Column("reviewer2_id", sa.BigInteger(), sa.ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True),
        sa.Column("review_note", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_kpm_syllabus_kp", "kp_mappings", ["syllabus_version", "knowledge_point"])
    op.create_index("ix_kpm_review_status", "kp_mappings", ["review_status"])
    op.create_index("ix_kpm_courseware", "kp_mappings", ["courseware_name"])

    # mapping_reviews 表
    op.create_table(
        "mapping_reviews",
        sa.Column("id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), primary_key=True, autoincrement=True),
        sa.Column("mapping_id", sa.BigInteger(), sa.ForeignKey("kp_mappings.id", ondelete="CASCADE"), nullable=False),
        sa.Column("reviewer_id", sa.BigInteger(), sa.ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True),
        sa.Column("review_round", sa.SmallInteger(), nullable=False),
        sa.Column("result", sa.String(16), nullable=False),
        sa.Column("review_level", sa.SmallInteger(), nullable=False, server_default="1"),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_mr_mapping_id", "mapping_reviews", ["mapping_id"])
    op.create_index("ix_mr_reviewer_id", "mapping_reviews", ["reviewer_id"])
    op.create_index("ix_mr_created_at", "mapping_reviews", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_mr_created_at", table_name="mapping_reviews")
    op.drop_index("ix_mr_reviewer_id", table_name="mapping_reviews")
    op.drop_index("ix_mr_mapping_id", table_name="mapping_reviews")
    op.drop_table("mapping_reviews")

    op.drop_index("ix_kpm_courseware", table_name="kp_mappings")
    op.drop_index("ix_kpm_review_status", table_name="kp_mappings")
    op.drop_index("ix_kpm_syllabus_kp", table_name="kp_mappings")
    op.drop_table("kp_mappings")

    op.drop_index("ix_wo_created_at", table_name="work_orders")
    op.drop_index("ix_wo_status", table_name="work_orders")
    op.drop_index("ix_wo_student_id", table_name="work_orders")
    op.drop_table("work_orders")

    op.drop_index("ix_teachers_role", table_name="teachers")
    op.drop_index("ix_teachers_teacher_no", table_name="teachers")
    op.drop_table("teachers")
