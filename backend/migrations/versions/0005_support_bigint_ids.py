"""Convert support telegram identifiers to bigint.

Revision ID: 0005_support_bigint_ids
Revises: 0004_support_ticket_status
"""
from typing import Sequence, Union

from alembic import op


revision: str = "0005_support_bigint_ids"
down_revision: Union[str, None] = "0004_support_ticket_status"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE support_messages ALTER COLUMN user_id TYPE BIGINT")
    op.execute("ALTER TABLE support_messages ALTER COLUMN admin_id TYPE BIGINT")
    op.execute("ALTER TABLE support_messages ALTER COLUMN support_message_id TYPE BIGINT")


def downgrade() -> None:
    op.execute("ALTER TABLE support_messages ALTER COLUMN user_id TYPE INTEGER")
    op.execute("ALTER TABLE support_messages ALTER COLUMN admin_id TYPE INTEGER")
    op.execute("ALTER TABLE support_messages ALTER COLUMN support_message_id TYPE INTEGER")
