"""add tariff in transaction objects v2

Revision ID: f38e338c2ad7
Revises: 4e8971f389da
Create Date: 2025-02-15 16:30:24.872668

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f38e338c2ad7'
down_revision: Union[str, None] = '4e8971f389da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
