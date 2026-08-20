"""Add version column to flow

Revision ID: e4f5a6b7c8da
Revises: 4dfa692e02a7
Create Date: 2026-04-22 00:00:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e4f5a6b7c8da"
down_revision = "4dfa692e02a7"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "flow",
        sa.Column("version", sa.String(50), nullable=True),
    )


def downgrade():
    op.drop_column("flow", "version")
