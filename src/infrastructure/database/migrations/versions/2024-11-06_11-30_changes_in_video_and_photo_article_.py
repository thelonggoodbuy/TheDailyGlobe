"""changes in video and photo article sections

Revision ID: 29c4e35e8b35
Revises: b75f0aac8455
Create Date: 2024-11-06 11:30:10.500893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29c4e35e8b35'
down_revision: Union[str, None] = 'b75f0aac8455'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article_section_with_slide_show', sa.Column('author', sa.String(length=255), nullable=False))
    op.add_column('article_section_with_video', sa.Column('title', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article_section_with_video', 'title')
    op.drop_column('article_section_with_slide_show', 'author')
    # ### end Alembic commands ###
