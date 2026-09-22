from datetime import datetime

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.models import Admin
from app.sales.models import Sale
from app.users.models import User


async def get_sales_rating(session: AsyncSession, start_date: datetime):
    result = await session.execute(
        select(
            Admin.telegram_id,
            func.coalesce(User.first_name, User.username, Admin.telegram_id).label("name"),
            func.count(Sale.id).label("subscriptions"),
            func.coalesce(func.sum(Sale.amount), 0).label("amount"),
        )
        .join(Sale, Admin.id == Sale.admin_id)
        .outerjoin(User, User.telegram_id == Admin.telegram_id)
        .where(Sale.created_at >= start_date)
        .group_by(Admin.id, User.first_name, User.username)
        .order_by(desc("subscriptions"))
    )

    rows = result.all()
    return [
        {
            "name": str(row.name),
            "subscriptions": row.subscriptions,
            "amount": row.amount,
        }
        for row in rows
    ]
