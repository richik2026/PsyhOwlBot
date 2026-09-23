from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.service import get_admin_by_telegram_id
from app.bot.states.reels import ReelsStates
from app.reels.service import add_reels

router = Router()


@router.message(ReelsStates.waiting_for_amount)
async def save_reels_amount(message: Message, state: FSMContext, session: AsyncSession):
    if not message.text or not message.text.isdigit():
        await message.answer("Введите число рилсов цифрами")
        return

    admin = await get_admin_by_telegram_id(session, message.from_user.id)
    if not admin or not admin.is_active or admin.role not in {"ADMIN", "SUPER_ADMIN"}:
        await state.clear()
        await message.answer("Эта команда доступна только администраторам")
        return

    await add_reels(session, admin.id, int(message.text))
    await session.commit()

    await state.clear()
    await message.answer("Благодарю вас за работу, коллега")
