"""Add default_parameters column to deployment

Revision ID: f5a6b7c8d9e0
Revises: 09a9e091e578
Create Date: 2026-04-22 01:00:00.000000

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f5a6b7c8d9e0"
down_revision = "09a9e091e578"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "deployment",
        sa.Column(
            "default_parameters",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )


def downgrade():
    op.drop_column("deployment", "default_parameters")
