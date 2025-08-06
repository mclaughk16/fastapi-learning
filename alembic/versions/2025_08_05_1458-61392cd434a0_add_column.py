"""add column

Revision ID: 61392cd434a0
Revises: 0c2a27b65bfa
Create Date: 2025-08-05 14:58:54.185162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61392cd434a0'
down_revision: Union[str, Sequence[str], None] = '0c2a27b65bfa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('test_table', sa.Column('updated_at', sa.DateTime))


def downgrade() -> None:
    op.drop_column('test_table', 'updated_at')
    pass
