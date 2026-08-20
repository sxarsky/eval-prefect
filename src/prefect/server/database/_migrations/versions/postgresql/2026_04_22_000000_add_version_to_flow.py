"""Add version column to flow

Revision ID: e4f5a6b7c8d9
Revises: 09a9e091e578
Create Date: 2026-04-22 00:00:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e4f5a6b7c8d9"
down_revision = "09a9e091e578"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "flow",
        sa.Column("version", sa.String(50), nullable=True),
    )


def downgrade():
    op.drop_column("flow", "version")
