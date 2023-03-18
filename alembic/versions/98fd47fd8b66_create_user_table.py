"""Create user table

Revision ID: 98fd47fd8b66
Revises: 85428979bc54
Create Date: 2023-03-18 22:24:32.784631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "98fd47fd8b66"
down_revision = "85428979bc54"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    pass


def downgrade():
    op.drop_table("users")
    pass
