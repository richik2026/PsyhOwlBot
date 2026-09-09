from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.models import Admin
from app.users.models import User
from app.reels.models import AdminReels


async def get_admin_dashboard(session: AsyncSession, admin: Admin) -> dict:
    users_result = await session.execute(
        select(func.count(User.id)).where(User.referrer_admin_id == admin.id)
    )
    users_count = users_result.scalar_one()

    reels_result = await session.execute(
        select(func.coalesce(func.sum(AdminReels.number_of_reels), 0)).where(
            AdminReels.admin_id == admin.id
        )
    )

    return {
        "role": admin.role,
        "users_count": users_count,
        "reels_count": reels_result.scalar_one(),
    }


def format_admin_dashboard(data: dict) -> str:
    return (
        "🦉 <b>Твоя статистика</b>\n\n"
        f"👤 Должность: {data['role']}\n\n"
        f"👥 Привлечено пользователей: {data['users_count']}\n\n"
        f"🎬 Reels: {data['reels_count']}"
    )
