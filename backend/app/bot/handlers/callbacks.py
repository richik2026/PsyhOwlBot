from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.dashboard import format_admin_dashboard, get_admin_dashboard
from app.admins.service import get_admin_by_telegram_id
from app.bot.keyboards.admin import admin_menu
from app.bot.states.reels import ReelsStates

router = Router()


async def is_admin(session: AsyncSession, telegram_id: int):
    admin = await get_admin_by_telegram_id(session, telegram_id)
    return admin and admin.is_active and admin.role in {"ADMIN", "SUPER_ADMIN"}


@router.callback_query(F.data == "admin_panel")
async def admin_panel_callback(callback: CallbackQuery, session: AsyncSession):
    admin = await get_admin_by_telegram_id(session, callback.from_user.id)

    if not admin or not admin.is_active or admin.role not in {"ADMIN", "SUPER_ADMIN"}:
        await callback.answer("Эта команда доступна только администраторам", show_alert=True)
        return

    data = await get_admin_dashboard(session, admin)

    await callback.message.edit_text(
        format_admin_dashboard(data),
        parse_mode="HTML",
        reply_markup=admin_menu(),
    )
    await callback.answer()


@router.callback_query(F.data == "add_reels")
async def add_reels_callback(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    if not await is_admin(session, callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    await state.set_state(ReelsStates.waiting_for_amount)
    await callback.message.answer("Введите количество рилсов, которое вы хотите добавить:")
    await callback.answer()
