"""delete refresh-token and blacklisted-token tables

Revision ID: 86f68104fe8a
Revises: a552502eca2f
Create Date: 2025-08-05 16:59:24.544461

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86f68104fe8a'
down_revision: Union[str, Sequence[str], None] = 'a552502eca2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_table('token_blacklist')
    op.drop_table('refresh_token')


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        'token_blacklist',
        sa.Column('token_id', sa.Integer(), primary_key=True),
        sa.Column('token', sa.Text(), nullable=False, unique=True),
        sa.Column('is_blacklisted', sa.Boolean(), server_default=sa.text('true')),
    )

    op.create_table(
        'refresh_token',
        sa.Column('refresh_token_id', sa.Integer(), primary_key=True),
        sa.Column('refresh_token', sa.Text(), nullable=False, unique=True, index=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column('is_expired', sa.Boolean(), server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
