"""error in index name

Revision ID: 22f7518d10db
Revises: ee62c2076639
Create Date: 2024-11-27 19:02:16.851944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22f7518d10db'
down_revision: Union[str, None] = 'ee62c2076639'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article_section_with_slide_show', sa.Column('index_number_in_article', sa.Integer(), nullable=False))
    op.drop_column('article_section_with_slide_show', 'intex_number_in_article')
    op.add_column('article_section_with_video', sa.Column('index_number_in_article', sa.Integer(), nullable=False))
    op.drop_column('article_section_with_video', 'intex_number_in_article')
    op.add_column('article_sections_with_plain_text', sa.Column('index_number_in_article', sa.Integer(), nullable=False))
    op.drop_column('article_sections_with_plain_text', 'intex_number_in_article')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article_sections_with_plain_text', sa.Column('intex_number_in_article', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('article_sections_with_plain_text', 'index_number_in_article')
    op.add_column('article_section_with_video', sa.Column('intex_number_in_article', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('article_section_with_video', 'index_number_in_article')
    op.add_column('article_section_with_slide_show', sa.Column('intex_number_in_article', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('article_section_with_slide_show', 'index_number_in_article')
    # ### end Alembic commands ###