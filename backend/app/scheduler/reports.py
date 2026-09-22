from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.ext.asyncio import AsyncSession

from app.ratings.formatter import format_reels_rating, format_sales_rating
from app.ratings.reels import get_reels_rating
from app.ratings.sales import get_sales_rating

MOSCOW_TZ = ZoneInfo("Europe/Moscow")

SALES_GROUP_ID = -1005476446888
REELS_GROUP_ID = -1001004405299682


async def send_daily_sales_report(bot, session: AsyncSession):
    """Send daily sales leaderboard to Telegram sales group."""
    start_date = datetime.now(MOSCOW_TZ).replace(hour=0, minute=0, second=0, microsecond=0)
    rating = await get_sales_rating(session, start_date)

    await bot.send_message(
        SALES_GROUP_ID,
        format_sales_rating(rating),
    )


async def send_daily_reels_report(bot, session: AsyncSession):
    """Send daily reels leaderboard to Telegram reels group."""
    start_date = datetime.now(MOSCOW_TZ).replace(hour=0, minute=0, second=0, microsecond=0)
    rating = await get_reels_rating(session, start_date)

    await bot.send_message(
        REELS_GROUP_ID,
        format_reels_rating(rating),
    )


def is_report_time(now: datetime | None = None) -> bool:
    now = now or datetime.now(MOSCOW_TZ)
    return now.hour == 23 and now.minute == 59
