"""Add fields for description and registration id in unregistered device model

Revision ID: 93ac3439a204
Revises: 51711c608cc3
Create Date: 2024-11-13 11:16:30.814397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '93ac3439a204'
down_revision: Union[str, None] = '51711c608cc3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('viewing', sa.Integer(), nullable=True))
    op.add_column('articles', sa.Column('is_premium', sa.Boolean(), nullable=True))
    op.drop_column('subscriptions', 'subscription_type')
    op.add_column('unregistered_devices', sa.Column('registration_id', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('unregistered_devices', 'registration_id')
    op.add_column('subscriptions', sa.Column('subscription_type', postgresql.ENUM('PREMIUM', 'PLUS', name='subscription_type'), autoincrement=False, nullable=False))
    op.drop_column('articles', 'is_premium')
    op.drop_column('articles', 'viewing')
    # ### end Alembic commands ###
