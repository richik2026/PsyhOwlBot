from datetime import date, datetime

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.reels.models import AdminReels


async def add_reels(
    session: AsyncSession,
    admin_id: int,
    number_of_reels: int,
) -> AdminReels:
    item = AdminReels(
        admin_id=admin_id,
        number_of_reels=number_of_reels,
        date=datetime.utcnow(),
    )
    session.add(item)
    await session.flush()
    return item


async def get_reels_rating_today(session: AsyncSession, limit: int = 10):
    today = date.today()

    result = await session.execute(
        select(
            AdminReels.admin_id,
            func.sum(AdminReels.number_of_reels).label("total"),
        )
        .where(func.date(AdminReels.date) == today)
        .group_by(AdminReels.admin_id)
        .order_by(desc("total"))
        .limit(limit)
    )

    return result.all()
