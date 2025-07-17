"""update task table

Revision ID: 2f5ea9e1d5ce
Revises: fa0268355e9c
Create Date: 2025-07-16 20:43:02.799393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f5ea9e1d5ce'
down_revision: Union[str, None] = 'fa0268355e9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
