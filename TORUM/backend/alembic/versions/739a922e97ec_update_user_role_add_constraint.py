"""update user-role: add constraint

Revision ID: 739a922e97ec
Revises: fc0600dcc981
Create Date: 2025-08-04 03:02:01.813522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '739a922e97ec'
down_revision: Union[str, Sequence[str], None] = 'fc0600dcc981'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Upgrade schema."""
    op.execute("ALTER TABLE users ADD CONSTRAINT valid_user_role CHECK (user_role IN ('user', 'moderator', 'admin'))")

def downgrade():
    """Downgrade schema."""
    op.execute("ALTER TABLE users DROP CONSTRAINT valid_user_role")
