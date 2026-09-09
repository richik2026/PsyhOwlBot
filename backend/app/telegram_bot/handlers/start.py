from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.service import get_or_create_user

from ..keyboards import main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, db_session: AsyncSession):
    await get_or_create_user(
        session=db_session,
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
    )

    await message.answer(
        "Рад тебя видеть у себя в гостях, о чём хочешь поговорить?",
        reply_markup=main_menu_keyboard(),
    )
