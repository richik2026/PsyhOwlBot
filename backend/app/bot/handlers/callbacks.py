from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.admin import open_admin_panel
from app.bot.states.reels import ReelsStates
from app.admins.service import get_admin_by_telegram_id

router = Router()


async def is_admin(session: AsyncSession, telegram_id: int, username: str | None = None):
    admin = await get_admin_by_telegram_id(session, telegram_id)
    return admin and admin.is_active


@router.callback_query(F.data == "admin_panel")
async def admin_panel_callback(callback: CallbackQuery, session: AsyncSession):
    await open_admin_panel(
        session,
        callback.from_user.id,
        callback.message.answer,
    )
    await callback.answer()


@router.callback_query(F.data == "add_reels")
async def add_reels_callback(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    if not await is_admin(session, callback.from_user.id, callback.from_user.username):
        await callback.answer("Нет доступа", show_alert=True)
        return

    await state.set_state(ReelsStates.waiting_for_amount)
    await callback.message.answer("Введите количество рилсов, которое вы хотите добавить:")
    await callback.answer()
