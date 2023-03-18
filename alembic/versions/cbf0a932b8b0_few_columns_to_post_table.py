"""few columns to post table

Revision ID: cbf0a932b8b0
Revises: 964868e4e228
Create Date: 2023-03-18 22:26:55.692180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cbf0a932b8b0"
down_revision = "964868e4e228"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    op.add_column("posts", sa.Column("owner_email", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "owner_email")
    op.drop_column("posts", "created_at")
    pass
