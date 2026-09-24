from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.models import Admin
from app.users.models import User
from app.reels.models import AdminReels
from app.sales.models import Sale


async def get_admin_dashboard(session: AsyncSession, admin: Admin) -> dict:
    users_result = await session.execute(
        select(func.count(User.id)).where(User.referrer_admin_id == admin.id)
    )
    users_count = users_result.scalar_one()

    sales_result = await session.execute(
        select(func.count(Sale.id)).where(Sale.admin_id == admin.id)
    )
    subscriptions_count = sales_result.scalar_one()

    revenue_result = await session.execute(
        select(func.coalesce(func.sum(Sale.amount), 0)).where(
            Sale.admin_id == admin.id
        )
    )
    revenue = revenue_result.scalar_one()

    reels_result = await session.execute(
        select(func.coalesce(func.sum(AdminReels.number_of_reels), 0)).where(
            AdminReels.admin_id == admin.id
        )
    )

    ranking_result = await session.execute(
        select(
            Admin.id,
            func.count(Sale.id).label("sales_count")
        )
        .join(Sale, Admin.id == Sale.admin_id)
        .group_by(Admin.id)
        .order_by(func.count(Sale.id).desc())
    )

    ranking = [row.id for row in ranking_result.all()]
    rating_place = ranking.index(admin.id) + 1 if admin.id in ranking else "—"

    return {
        "role": admin.role,
        "users_count": users_count,
        "subscriptions_count": subscriptions_count,
        "revenue": revenue,
        "rating_place": rating_place,
        "reels_count": reels_result.scalar_one(),
    }


def format_admin_dashboard(data: dict) -> str:
    return (
        "🦉 <b>Комнада Администратора</b> 🦉\n"
        "—————————————————\n"
        f"👑 Должность: {data['role']}\n"
        "—————————————————\n"
        f"👥 Привлечено пользователей: {data['users_count']}\n"
        f"💷 Из них оплатили: {data['subscriptions_count']}\n"
        f"💰 На сумму: {data['revenue']} ₽\n"
        "—————————————————\n"
        f"🔝 Место в рейтинге: {data['rating_place']}\n"
        "—————————————————\n"
        f"🎬 Всего опубликовано Reels: {data['reels_count']}"
    )
