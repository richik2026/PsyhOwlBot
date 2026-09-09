"""Create reels, sales and subscriptions tables.

Revision ID: 0002_commercial_tables
Revises: 0001_core_foundation
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_commercial_tables"
down_revision: Union[str, None] = "0001_core_foundation"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "admin_reels",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("admin_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("number_of_reels", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["admin_id"], ["admins.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_admin_reels_admin_id", "admin_reels", ["admin_id"])
    op.create_index("ix_admin_reels_date", "admin_reels", ["date"])

    op.create_table(
        "sales",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("admin_id", sa.Integer(), nullable=True),
        sa.Column("provider", sa.String(length=50), nullable=False, server_default="tribute"),
        sa.Column("provider_payment_id", sa.String(length=255), nullable=True),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="RUB"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["admin_id"], ["admins.id"], ondelete="SET NULL"),
        sa.UniqueConstraint("provider_payment_id", name="uq_sales_provider_payment_id"),
    )
    op.create_index("ix_sales_user_id", "sales", ["user_id"])
    op.create_index("ix_sales_admin_id", "sales", ["admin_id"])
    op.create_index("ix_sales_created_at", "sales", ["created_at"])

    op.create_table(
        "subscriptions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("active_until", sa.DateTime(), nullable=False),
        sa.Column("total_seconds", sa.Integer(), nullable=False, server_default="216000"),
        sa.Column("used_seconds", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("daily_limit_seconds", sa.Integer(), nullable=False, server_default="7200"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("user_id", name="uq_subscriptions_user_id"),
    )
    op.create_index("ix_subscriptions_user_id", "subscriptions", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_subscriptions_user_id", table_name="subscriptions")
    op.drop_table("subscriptions")

    op.drop_index("ix_sales_created_at", table_name="sales")
    op.drop_index("ix_sales_admin_id", table_name="sales")
    op.drop_index("ix_sales_user_id", table_name="sales")
    op.drop_table("sales")

    op.drop_index("ix_admin_reels_date", table_name="admin_reels")
    op.drop_index("ix_admin_reels_admin_id", table_name="admin_reels")
    op.drop_table("admin_reels")
