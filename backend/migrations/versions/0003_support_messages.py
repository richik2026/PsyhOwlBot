"""Create support messages table.

Revision ID: 0003_support_messages
Revises: 0002_commercial_tables
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0003_support_messages"
down_revision: Union[str, None] = "0002_commercial_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "support_messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("support_message_id", sa.Integer(), nullable=False),
        sa.Column("admin_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["admin_id"], ["admins.id"], ondelete="SET NULL"),
    )

    op.create_index(
        "ix_support_messages_support_message_id",
        "support_messages",
        ["support_message_id"],
    )
    op.create_index(
        "ix_support_messages_user_id",
        "support_messages",
        ["user_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_support_messages_user_id", table_name="support_messages")
    op.drop_index("ix_support_messages_support_message_id", table_name="support_messages")
    op.drop_table("support_messages")
