from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.main import main_menu
from app.referrals.service import resolve_referrer_admin_id
from app.users.service import get_or_create_user

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, session: AsyncSession):
    args = message.text.split(maxsplit=1)
    start_parameter = args[1] if len(args) > 1 else None

    referrer_admin_id = await resolve_referrer_admin_id(session, start_parameter)

    await get_or_create_user(
        session,
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        referrer_admin_id=referrer_admin_id,
    )

    await session.commit()

    await message.answer(
        "Рад тебя видеть у Совёнка Криша 🦉\n\nО чём хочешь поговорить?",
        reply_markup=main_menu(),
    )
