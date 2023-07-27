# noqa: INP001 it's a migration module, no need for a package
"""
Message: "add url".

- Revision ID: 65bb7b08cbaa
- Previous: None
- Create Date: 2023-06-13 16:09:58.426331
"""


import sqlalchemy as sa
from alembic import op

revision = "65bb7b08cbaa"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database to the next revision."""
    op.create_table(
        "url",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("target", sa.String(), nullable=False),
        sa.Column("clicks", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade database to the previous revision."""
    op.drop_table("url")
