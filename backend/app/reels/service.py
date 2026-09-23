from datetime import date, datetime

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.reels.models import AdminReels


async def add_reels(session: AsyncSession, admin_id: int, number_of_reels: int) -> AdminReels:
    today = date.today()

    result = await session.execute(
        select(AdminReels).where(
            AdminReels.admin_id == admin_id,
            func.date(AdminReels.date) == today,
        )
    )

    item = result.scalar_one_or_none()

    if item:
        item.number_of_reels = number_of_reels
        item.date = datetime.utcnow()
        await session.flush()
        return item

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
        select(AdminReels)
        .where(func.date(AdminReels.date) == today)
        .order_by(desc(AdminReels.number_of_reels))
        .limit(limit)
    )

    return result.scalars().all()
