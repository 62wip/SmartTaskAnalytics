"""update table

Revision ID: fa0268355e9c
Revises: 77b44866b5f9
Create Date: 2025-07-16 19:44:02.017494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa0268355e9c'
down_revision: Union[str, None] = '77b44866b5f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
