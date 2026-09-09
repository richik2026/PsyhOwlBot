"""Create core user, admin, referral and settings tables.

Revision ID: 0001_core_foundation
Revises: None
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_core_foundation"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "admins",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="ADMIN"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("telegram_id", name="uq_admins_telegram_id"),
    )
    op.create_index("ix_admins_telegram_id", "admins", ["telegram_id"])

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=True),
        sa.Column("first_name", sa.String(length=255), nullable=True),
        sa.Column("referrer_admin_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["referrer_admin_id"], ["admins.id"], ondelete="SET NULL"),
        sa.UniqueConstraint("telegram_id", name="uq_users_telegram_id"),
    )
    op.create_index("ix_users_telegram_id", "users", ["telegram_id"])
    op.create_index("ix_users_referrer_admin_id", "users", ["referrer_admin_id"])

    op.create_table(
        "settings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("key", sa.String(length=255), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("key", name="uq_settings_key"),
    )
    op.create_index("ix_settings_key", "settings", ["key"])

    op.create_table(
        "referral_links",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("admin_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["admin_id"], ["admins.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("code", name="uq_referral_links_code"),
    )
    op.create_index("ix_referral_links_admin_id", "referral_links", ["admin_id"])
    op.create_index("ix_referral_links_code", "referral_links", ["code"])


def downgrade() -> None:
    op.drop_index("ix_referral_links_code", table_name="referral_links")
    op.drop_index("ix_referral_links_admin_id", table_name="referral_links")
    op.drop_table("referral_links")

    op.drop_index("ix_settings_key", table_name="settings")
    op.drop_table("settings")

    op.drop_index("ix_users_referrer_admin_id", table_name="users")
    op.drop_index("ix_users_telegram_id", table_name="users")
    op.drop_table("users")

    op.drop_index("ix_admins_telegram_id", table_name="admins")
    op.drop_table("admins")
