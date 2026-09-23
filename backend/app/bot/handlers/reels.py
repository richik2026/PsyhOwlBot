from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.service import get_admin_by_telegram_id
from app.bot.states.reels import ReelsStates
from app.reels.service import add_reels, get_reels_rating_today

router = Router()


async def is_admin(session: AsyncSession, telegram_id: int):
    admin = await get_admin_by_telegram_id(session, telegram_id)
    return admin and admin.is_active and admin.role in {"ADMIN", "SUPER_ADMIN"}


@router.callback_query(F.data == "add_reels")
async def add_reels_start(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    if not await is_admin(session, callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    await state.set_state(ReelsStates.waiting_for_amount)
    await callback.message.answer("Введите количество рилсов, которое вы хотите добавить:")
    await callback.answer()


@router.message(ReelsStates.waiting_for_amount)
async def save_reels_amount(message: Message, state: FSMContext, session: AsyncSession):
    if not message.text or not message.text.isdigit():
        await message.answer("Введите число рилсов цифрами")
        return

    admin = await get_admin_by_telegram_id(session, message.from_user.id)
    if not admin or not admin.is_active or admin.role not in {"ADMIN", "SUPER_ADMIN"}:
        await state.clear()
        return

    await add_reels(session, admin.id, int(message.text))
    await session.commit()

    rating = await get_reels_rating_today(session)
    place = next((i for i, item in enumerate(rating, 1) if item.admin_id == admin.id), None)

    await state.clear()
    await message.answer(
        "Благодарю вас за работу, коллега\n\n"
        f"Ваш результат добавлен в статистику. Место за сегодня: {place or '-'}"
    )
