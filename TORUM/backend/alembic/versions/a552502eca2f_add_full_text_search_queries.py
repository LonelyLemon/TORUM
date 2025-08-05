"""Add full-text search queries

Revision ID: a552502eca2f
Revises: 1dd0b1e19c5a
Create Date: 2025-08-04 20:53:48.591836

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a552502eca2f'
down_revision: Union[str, Sequence[str], None] = '1dd0b1e19c5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('search_vector', sa.dialects.postgresql.TSVECTOR))
    op.add_column('reading_documents', sa.Column('search_vector', sa.dialects.postgresql.TSVECTOR))

    op.execute("""
        UPDATE posts 
        SET search_vector = to_tsvector('english', post_title || ' ' || coalesce(post_content, ''))
    """)
    op.execute("""
        UPDATE reading_documents 
        SET search_vector = to_tsvector('english', docs_title || ' ' || coalesce(docs_description, '') || ' ' || docs_tags)
    """)
    
    op.create_index('idx_post_search', 'posts', ['search_vector'], postgresql_using='gin')
    op.create_index('idx_docs_search', 'reading_documents', ['search_vector'], postgresql_using='gin')
    
    op.execute("""
        CREATE TRIGGER tsvector_update_posts
        BEFORE INSERT OR UPDATE ON posts
        FOR EACH ROW
        EXECUTE FUNCTION
        tsvector_update_trigger(search_vector, 'pg_catalog.english', post_title, post_content)
    """)
    op.execute("""
        CREATE TRIGGER tsvector_update_docs
        BEFORE INSERT OR UPDATE ON reading_documents
        FOR EACH ROW
        EXECUTE FUNCTION
        tsvector_update_trigger(search_vector, 'pg_catalog.english', docs_title, docs_description, docs_tags)
    """)

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS tsvector_update_posts ON posts")
    op.execute("DROP TRIGGER IF EXISTS tsvector_update_docs ON reading_documents")
    op.drop_index('idx_post_search', table_name='posts')
    op.drop_index('idx_docs_search', table_name='reading_documents')
    op.drop_column('posts', 'search_vector')
    op.drop_column('reading_documents', 'search_vector')
