"""Add assignee_id to work_orders

Revision ID: 20250108_0008
Revises: 0007_oj_anticheat
Create Date: 2025-01-08 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite


# revision identifiers, used by Alembic.
revision: str = '20250108_0008'
down_revision: Union[str, None] = '0007_oj_anticheat'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    dialect = op.get_context().dialect.name

    # 添加 assignee_id 字段（被分配处理工单的老师）
    op.add_column('work_orders', sa.Column('assignee_id', sa.BigInteger(), nullable=True))

    # SQLite 不支持 ALTER 添加外键，跳过；PostgreSQL 正常添加
    if dialect != 'sqlite':
        op.create_foreign_key(
            'fk_work_orders_assignee_id_teachers',
            'work_orders', 'teachers',
            ['assignee_id'], ['id'],
            ondelete='SET NULL'
        )

    op.create_index('ix_wo_assignee_id', 'work_orders', ['assignee_id'])

    # 已有数据：assignee_id 默认等于创建者 teacher_id
    op.execute('UPDATE work_orders SET assignee_id = teacher_id')


def downgrade() -> None:
    dialect = op.get_context().dialect.name

    op.drop_index('ix_wo_assignee_id', table_name='work_orders')

    if dialect != 'sqlite':
        op.drop_constraint('fk_work_orders_assignee_id_teachers', 'work_orders', type_='foreignkey')

    op.drop_column('work_orders', 'assignee_id')
