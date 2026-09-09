from datetime import datetime, timezone

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.models import Admin
from app.reels.models import AdminReels


async def get_reels_rating(session: AsyncSession, start_date: datetime):
    result = await session.execute(
        select(
            Admin.telegram_id,
            func.coalesce(func.sum(AdminReels.number_of_reels), 0).label("reels"),
        )
        .join(AdminReels, Admin.id == AdminReels.admin_id)
        .where(AdminReels.date >= start_date)
        .group_by(Admin.id)
        .order_by(desc("reels"))
    )

    rows = result.all()
    return [{"name": str(row.telegram_id), "reels": row.reels} for row in rows]
