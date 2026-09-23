"""Remove support user foreign key.

Revision ID: 0006_support_remove_user_fk
Revises: 0005_support_bigint_ids
"""
from typing import Sequence, Union

from alembic import op

revision: str = "0006_support_remove_user_fk"
down_revision: Union[str, None] = "0005_support_bigint_ids"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "support_messages_user_id_fkey",
        "support_messages",
        type_="foreignkey",
    )


def downgrade() -> None:
    op.create_foreign_key(
        "support_messages_user_id_fkey",
        "support_messages",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
