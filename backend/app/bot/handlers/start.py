from datetime import datetime

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.models import Admin
from app.admins.service import ensure_whitelist_admin
from app.bot.keyboards.main import main_menu
from app.referrals.service import resolve_referrer_admin_id
from app.subscriptions.models import Subscription
from app.subscriptions.service import has_active_access, remaining_seconds
from app.users.models import User
from app.users.service import get_or_create_user

router = Router()


async def get_subscription(session: AsyncSession, user_id: int):
    result = await session.execute(select(Subscription).where(Subscription.user_id == user_id))
    return result.scalar_one_or_none()


@router.message(CommandStart())
async def start_handler(message: Message, session: AsyncSession):
    args = message.text.split(maxsplit=1)
    start_parameter = args[1] if len(args) > 1 else None

    referrer_admin_id = await resolve_referrer_admin_id(session, start_parameter)

    admin = await ensure_whitelist_admin(
        session,
        telegram_id=message.from_user.id,
        username=message.from_user.username,
    )

    user, _ = await get_or_create_user(
        session,
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        referrer_admin_id=referrer_admin_id,
    )

    subscription = await get_subscription(session, user.id)
    is_admin = bool(admin and admin.role in {"ADMIN", "SUPER_ADMIN"} and admin.is_active)

    await session.commit()

    name = message.from_user.first_name or message.from_user.username or "друг"

    if is_admin:
        text = (
            f"Добро пожаловать, {name}!🦉\n\n"
            "Меня зовут Криш, и я очень рад приветствовать тебя🫂\n\n"
            "На данный момент твоя подписка: Активна✅\n\n"
            "Тебе доступно ещё: 2222 часов разговоров со мной⌛️\n\n"
            "Подписка закончится через: Никогда. 🗓"
        )
    elif has_active_access(subscription):
        days = max(0, (subscription.active_until - datetime.utcnow()).days)
        hours = remaining_seconds(subscription) // 3600
        text = (
            f"Добро пожаловать, {name}!🦉\n\n"
            "Меня зовут Криш, и я очень рад приветствовать тебя🫂\n\n"
            "На данный момент твоя подписка: Активна✅\n\n"
            f"Тебе доступно ещё: {hours} часов разговоров со мной⌛️\n\n"
            f"Подписка закончится через: {days} дней. 🗓"
        )
    else:
        text = (
            f"Добро пожаловать, {name}!🦉\n\n"
            "🫂 Меня зовут Криш\n\n"
            "👩‍🏫 Я — современный инновационный психологический друг,\n"
            "обученный на материалах лучших мировых университетов📚\n\n"
            "📈Мы сэкономили деньги на психологах более чем 100 людям,\n"
            "а возможно даже дали гораздо лучший эффект☝️\n\n"
            "Для того, чтобы воспользоваться моими услугами, необходимо активировать подписку"
        )

    await message.answer(
        text,
        reply_markup=main_menu(is_admin=is_admin, has_subscription=is_admin or has_active_access(subscription)),
    )
