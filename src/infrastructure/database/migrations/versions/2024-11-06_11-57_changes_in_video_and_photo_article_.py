"""changes in video and photo article sections

Revision ID: 51711c608cc3
Revises: 29c4e35e8b35
Create Date: 2024-11-06 11:57:17.619909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51711c608cc3'
down_revision: Union[str, None] = '29c4e35e8b35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article_section_with_video', sa.Column('image_preview', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article_section_with_video', 'image_preview')
    # ### end Alembic commands ###