"""create first table

Revision ID: 0c2a27b65bfa
Revises: 
Create Date: 2025-08-05 14:53:36.600808

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c2a27b65bfa'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'test_table',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('age', sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('test_table')
