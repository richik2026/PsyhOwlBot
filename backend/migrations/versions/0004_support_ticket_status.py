"""Add support ticket status.

Revision ID: 0004_support_ticket_status
Revises: 0003_support_messages
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0004_support_ticket_status"
down_revision: Union[str, None] = "0003_support_messages"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "support_messages",
        sa.Column("status", sa.String(length=32), nullable=False, server_default="new")
    )
    op.alter_column("support_messages", "status", server_default=None)


def downgrade() -> None:
    op.drop_column("support_messages", "status")
