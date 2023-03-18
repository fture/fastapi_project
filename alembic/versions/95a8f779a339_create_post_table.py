"""Create post table

Revision ID: 95a8f779a339
Revises: 
Create Date: 2023-03-18 22:21:37.572391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "95a8f779a339"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.UUID(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )
    pass


def downgrade():
    op.drop_table("posts")
    pass
