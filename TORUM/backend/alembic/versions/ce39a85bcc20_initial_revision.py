"""initial revision

Revision ID: ce39a85bcc20
Revises: 
Create Date: 2025-08-01 03:28:51.264473

"""
import sqlalchemy as sa

from typing import Sequence, Union
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'ce39a85bcc20'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), primary_key=True, index=True, default=sa.text('gen_random_uuid()')),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('user_role', sa.String(), default="trader")
    )

    op.create_table(
        'posts',
        sa.Column('post_id', postgresql.UUID(as_uuid=True), index=True, primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('post_owner', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column('post_title', sa.String(), nullable=False),
        sa.Column('post_content', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now())
    )

    op.create_table(
        'reading_documents',
        sa.Column('docs_id', postgresql.UUID(as_uuid=True), primary_key=True, index=True, default=sa.text('gen_random_uuid()')),
        sa.Column('docs_owner', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column('docs_title', sa.String(), nullable=False),
        sa.Column('docs_description', sa.Text()),
        sa.Column('docs_tags', sa.String(), server_default='Documents'),
        sa.Column('docs_file_path', sa.String(), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )

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
    
def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('refresh_token')
    op.drop_table('token_blacklist')
    op.drop_table('reading_documents')
    op.drop_table('posts')
    op.drop_table('users')
