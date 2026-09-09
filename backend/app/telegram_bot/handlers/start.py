from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.service import get_or_create_user
from app.referrals.service import get_admin_by_referral_code

from ..keyboards import main_menu_keyboard

router = Router()


@router.message(CommandStart(deep_link=True))
async def start_handler(message: Message, command, db_session: AsyncSession):
    referrer_admin_id = None

    if command.args:
        referrer_admin_id = await get_admin_by_referral_code(
            session=db_session,
            code=command.args.replace("adm_", ""),
        )

    await get_or_create_user(
        session=db_session,
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        referrer_admin_id=referrer_admin_id,
    )

    await message.answer(
        "Рад тебя видеть у себя в гостях, о чём хочешь поговорить?",
        reply_markup=main_menu_keyboard(),
    )
