"""update document constraints

Revision ID: 1dd0b1e19c5a
Revises: 739a922e97ec
Create Date: 2025-08-04 08:18:34.006568

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1dd0b1e19c5a'
down_revision: Union[str, Sequence[str], None] = '739a922e97ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TABLE reading_documents ADD CONSTRAINT check_docs_file_path_extension CHECK (lower(right(docs_file_path, 4)) IN ('.pdf', '.docx'))")
    op.execute("UPDATE reading_documents SET docs_file_path = docs_file_path WHERE lower(right(docs_file_path, 4)) IN ('.pdf', '.docx')")

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE reading_documents DROP CONSTRAINT IF EXISTS check_docs_file_path_extension")
