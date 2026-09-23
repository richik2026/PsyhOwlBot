"""Remove support admin foreign key.

Revision ID: 0007_support_remove_admin_fk
Revises: 0006_support_remove_user_fk
Create Date: 2026-09-23
"""

from alembic import op

revision = "0007_support_remove_admin_fk"
down_revision = "0006_support_remove_user_fk"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint(
        "support_messages_admin_id_fkey",
        "support_messages",
        type_="foreignkey",
    )


def downgrade():
    op.create_foreign_key(
        "support_messages_admin_id_fkey",
        "support_messages",
        "admins",
        ["admin_id"],
        ["telegram_id"],
    )
