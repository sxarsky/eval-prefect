"""Add default_parameters column to deployment

Revision ID: f5a6b7c8d9e1
Revises: 4dfa692e02a7
Create Date: 2026-04-22 01:00:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f5a6b7c8d9e1"
down_revision = "4dfa692e02a7"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "deployment",
        sa.Column("default_parameters", sa.JSON(), nullable=True),
    )


def downgrade():
    op.drop_column("deployment", "default_parameters")
