"""Add column post table

Revision ID: 85428979bc54
Revises: 95a8f779a339
Create Date: 2023-03-18 22:23:54.251844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "85428979bc54"
down_revision = "95a8f779a339"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
