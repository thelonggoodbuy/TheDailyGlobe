"""add extendet title in category

Revision ID: e92dcb009c43
Revises: 22f7518d10db
Create Date: 2024-12-13 14:30:54.818313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e92dcb009c43'
down_revision: Union[str, None] = '22f7518d10db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('extended_title', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('category', 'extended_title')
    # ### end Alembic commands ###