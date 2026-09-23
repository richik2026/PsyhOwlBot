from datetime import date, datetime

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.reels.models import AdminReels


ADMIN_USERNAMES = {
    "bo0odyaa": "bo0odyaa",
    "twystedgeniusbaby": "twystedgeniusbaby",
    "fib112358": "fib112358",
    "NSW27": "NSW27",
    "povarrrehka": "povarrrehka",
    "Metalheadzzz": "Metalheadzzz",
    "asakura_15": "asakura_15",
}


async def add_reels(session: AsyncSession, admin_id: int, number_of_reels: int):
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
    else:
        item = AdminReels(
            admin_id=admin_id,
            number_of_reels=number_of_reels,
            date=datetime.utcnow(),
        )
        session.add(item)

    await session.flush()
    return item


async def get_reels_rating_today(session: AsyncSession, limit: int = 10):
    result = await session.execute(
        select(AdminReels)
        .where(func.date(AdminReels.date) == date.today())
        .order_by(desc(AdminReels.number_of_reels))
        .limit(limit)
    )
    return result.scalars().all()


async def format_reels_rating(session: AsyncSession):
    items = await get_reels_rating_today(session)
    medals = ["🥇", "🥈", "🥉"]
    lines = ["📊 Рилсы за сегодня:"]

    for index, item in enumerate(items, 1):
        prefix = medals[index - 1] if index <= 3 else f"{index}."
        username = ADMIN_USERNAMES.get(str(item.admin_id), f"admin_{item.admin_id}")
        lines.append(f"{prefix} @{username} — {item.number_of_reels}")

    return "\n".join(lines)
