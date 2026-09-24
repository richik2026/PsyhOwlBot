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
    args = (message.text or "").split(maxsplit=1)
    start_parameter = args[1] if len(args) > 1 else None

    try:
        referrer_admin_id = await resolve_referrer_admin_id(session, start_parameter)
    except Exception:
        referrer_admin_id = None

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
    is_admin = bool(admin and admin.is_active and admin.role in {"ADMIN", "SUPER_ADMIN"})
    await session.commit()

    name = message.from_user.first_name or message.from_user.username or "друг"

    if is_admin:
        hours = "2222"
        finish = "Никогда"
    elif has_active_access(subscription):
        hours = str(remaining_seconds(subscription) // 3600)
        finish = f"{max(0, (subscription.active_until - datetime.utcnow()).days)} дней"
    else:
        hours = None
        finish = None

    if hours:
        text = (
            f"<b>Добро пожаловать, {name}</b>! 🦉\n\n"
            "Меня зовут Криш, и я очень рад приветствовать тебя 🫂\n"
            "━━━━━━━━━━━━━━\n"
            "🔶 Подписка: <u><i>Активна</i></u>✅\n"
            f"🔶 Доступно: <u><i>{hours} часов</i></u> разговора со мной ⌛️\n"
            "━━━━━━━━━━━━━━\n"
            f"Подписка закончится через: <u><i>{finish}</i></i></u>. 🗓"
        )
    else:
        text = (
            f"Добро пожаловать, <b>{name}</b>! 🦉\n\n"
            "🤍 <b>Меня зовут Криш</b>\n\n"
            "Я — современный инновационный психологический друг 🦉"
            "Меня обучали на материалах лучших мировых университетов, таких как:\n"
            "----------------------\n"
            "📚 Yale University — Introduction to Psychology (Paul Bloom)\n"
            "📚 MIT — Introduction to Psychology (9.00SC)\n"
            "📚 Cognitive Psychology / Human Behavior (Stanford University)\n"
            "----------------------\n\n"
            "🌍 И многих других!"
        )

    await message.answer_photo(
        FSInputFile(WELCOME_IMAGE),
        caption=text,
        parse_mode="HTML",
        reply_markup=main_menu(is_admin=is_admin, has_subscription=bool(hours)),
    )
