from datetime import datetime

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.service import ensure_whitelist_admin
from app.bot.keyboards.main import main_menu
from app.referrals.service import resolve_referrer_admin_id
from app.subscriptions.models import Subscription
from app.subscriptions.service import has_active_access, remaining_seconds
from app.users.service import get_or_create_user

router = Router()

WELCOME_IMAGE = "app/bot/assets/Sovenok_Psiholog_Welcome_1280x720.jpg"


async def get_subscription(session: AsyncSession, user_id: int):
    result = await session.execute(select(Subscription).where(Subscription.user_id == user_id))
    return result.scalar_one_or_none()


@router.message(CommandStart())
async def start_handler(message: Message, session: AsyncSession):
    args = message.text.split(maxsplit=1)
    start_parameter = args[1] if len(args) > 1 else None

    await resolve_referrer_admin_id(session, start_parameter)
    admin = await ensure_whitelist_admin(session, message.from_user.id, message.from_user.username)

    user, _ = await get_or_create_user(
        session,
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
    )

    subscription = await get_subscription(session, user.id)
    is_admin = bool(admin and admin.is_active and admin.role in {"ADMIN", "SUPER_ADMIN"})
    await session.commit()

    name = message.from_user.first_name or message.from_user.username or "друг"

    if is_admin:
        hours = "2222"
        end = "Никогда"
    elif has_active_access(subscription):
        hours = str(remaining_seconds(subscription) // 3600)
        end = str(max(0, (subscription.active_until - datetime.utcnow()).days))
    else:
        hours = None
        end = None

    if hours:
        finish = "Никогда" if end == "Никогда" else f"{end} дней"
        text = (
            f"Добро пожаловать, <b>{name}</b>! 🦉\n\n"
            "Меня зовут Криш, и я очень рад приветствовать тебя 🫂\n\n"
            "━━━━━━━━━━━━━━\n\n"
            "🔶 Подписка: Активна ✅\n\n"
            f"🔶 Доступно: {hours} часов разговора со мной ⌛️\n\n"
            f"Подписка закончится через: {finish}. 🗓"
        )
    else:
        text = (
            f"Добро пожаловать, <b>{name}</b>! 🦉\n\n"
            "🫂 <b>Меня зовут Криш</b>\n\n"
            "Я — современный инновационный психологический друг 🦉"
        )

    await message.answer_photo(
        FSInputFile(WELCOME_IMAGE),
        caption=text,
        parse_mode="HTML",
        reply_markup=main_menu(is_admin=is_admin, has_subscription=bool(hours)),
    )
