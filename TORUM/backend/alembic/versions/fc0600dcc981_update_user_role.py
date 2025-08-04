"""update user-role

Revision ID: fc0600dcc981
Revises: ce39a85bcc20
Create Date: 2025-08-04 02:40:05.206688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc0600dcc981'
down_revision: Union[str, Sequence[str], None] = 'ce39a85bcc20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('users', 'user_role', server_default='user')
    op.execute("UPDATE users SET user_role = 'user' WHERE user_role = 'trader'")

def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'user_role', server_default='trader')
    op.execute("UPDATE users SET user_role = 'trader' WHERE user_role = 'user'")

