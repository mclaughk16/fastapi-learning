"""generate post table

Revision ID: 99734cfdee2b
Revises: a42464579957
Create Date: 2025-08-08 15:56:46.605730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99734cfdee2b'
down_revision: Union[str, Sequence[str], None] = 'a42464579957'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
