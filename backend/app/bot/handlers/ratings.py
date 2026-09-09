from datetime import datetime, timedelta, timezone

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.ratings.formatter import format_reels_rating, format_sales_rating
from app.ratings.reels import get_reels_rating
from app.ratings.sales import get_sales_rating

router = Router()


def _period_start(period: str) -> datetime:
    now = datetime.now(timezone.utc)
    if period == "today":
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    if period == "week":
        start = now - timedelta(days=now.weekday())
        return start.replace(hour=0, minute=0, second=0, microsecond=0)
    if period == "month":
        return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if period == "year":
        return now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


async def _send_sales(message: Message, session: AsyncSession, period: str) -> None:
    items = await get_sales_rating(session, _period_start(period))
    await message.answer(format_sales_rating(items))


async def _send_reels(message: Message, session: AsyncSession, period: str) -> None:
    items = await get_reels_rating(session, _period_start(period))
    await message.answer(format_reels_rating(items))


@router.message(Command("top", "toptoday"))
async def sales_today(message: Message, session: AsyncSession) -> None:
    await _send_sales(message, session, "today")


@router.message(Command("toptoweek"))
async def sales_week(message: Message, session: AsyncSession) -> None:
    await _send_sales(message, session, "week")


@router.message(Command("toptomonth"))
async def sales_month(message: Message, session: AsyncSession) -> None:
    await _send_sales(message, session, "month")


@router.message(Command("toptoyear"))
async def sales_year(message: Message, session: AsyncSession) -> None:
    await _send_sales(message, session, "year")


@router.message(Command("reelstoptoday"))
async def reels_today(message: Message, session: AsyncSession) -> None:
    await _send_reels(message, session, "today")


@router.message(Command("reelstopweek"))
async def reels_week(message: Message, session: AsyncSession) -> None:
    await _send_reels(message, session, "week")


@router.message(Command("reelstopmonth"))
async def reels_month(message: Message, session: AsyncSession) -> None:
    await _send_reels(message, session, "month")


@router.message(Command("reelstopyear"))
async def reels_year(message: Message, session: AsyncSession) -> None:
    await _send_reels(message, session, "year")
