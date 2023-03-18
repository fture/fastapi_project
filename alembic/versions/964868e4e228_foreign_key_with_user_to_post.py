"""foreign key with user to post

Revision ID: 964868e4e228
Revises: 98fd47fd8b66
Create Date: 2023-03-18 22:25:55.740551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "964868e4e228"
down_revision = "98fd47fd8b66"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.UUID(), nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade():
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
