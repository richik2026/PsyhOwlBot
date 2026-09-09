from datetime import datetime

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.models import Admin
from app.sales.models import Sale


async def get_sales_rating(session: AsyncSession, start_date: datetime):
    result = await session.execute(
        select(
            Admin.telegram_id,
            func.count(Sale.id).label("subscriptions"),
            func.coalesce(func.sum(Sale.amount), 0).label("amount"),
        )
        .join(Sale, Admin.id == Sale.admin_id)
        .where(Sale.created_at >= start_date)
        .group_by(Admin.id)
        .order_by(desc("subscriptions"))
    )

    rows = result.all()
    return [
        {
            "name": str(row.telegram_id),
            "subscriptions": row.subscriptions,
            "amount": row.amount,
        }
        for row in rows
    ]
