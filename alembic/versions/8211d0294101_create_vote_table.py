"""create vote table 

Revision ID: 8211d0294101
Revises: cbf0a932b8b0
Create Date: 2023-03-18 22:42:41.643247

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8211d0294101"
down_revision = "cbf0a932b8b0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "votes",
        sa.Column("post_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("like", sa.Boolean(), server_default="FALSE", nullable=False),
        sa.Column(
            "vote_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("comment", sa.Text(), server_default="FALSE", nullable=True),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("post_id", "user_id", name="vote_pk"),
    )

    op.create_unique_constraint(None, "posts", ["id"])
    op.create_unique_constraint(None, "users", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="unique")
    op.drop_constraint(None, "posts", type_="unique")

    op.drop_table("votes")
    # ### end Alembic commands ###
