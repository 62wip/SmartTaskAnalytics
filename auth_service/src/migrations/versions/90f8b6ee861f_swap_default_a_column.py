"""Swap default a column

Revision ID: 90f8b6ee861f
Revises: 272c7a82aa6f
Create Date: 2025-07-14 01:25:20.194676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90f8b6ee861f'
down_revision: Union[str, Sequence[str], None] = '272c7a82aa6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
