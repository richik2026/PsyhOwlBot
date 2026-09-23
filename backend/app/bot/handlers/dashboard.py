from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.dashboard import get_admin_dashboard, format_admin_dashboard
from app.admins.service import get_admin_by_telegram_id
from app.bot.keyboards.admin import admin_menu

router = Router()


async def show_admin_panel(target, session: AsyncSession):
    admin = await get_admin_by_telegram_id(session, target.from_user.id)

    if admin is None or not admin.is_active:
        await target.answer("Доступ только для администраторов")
        return

    data = await get_admin_dashboard(session, admin)
    await target.answer(
        format_admin_dashboard(data),
        reply_markup=admin_menu(),
    )


@router.message(lambda message: message.text == "📊 Админ-Панель")
async def admin_dashboard(message: Message, session: AsyncSession):
    await show_admin_panel(message, session)


@router.callback_query(F.data == "admin_panel")
async def admin_dashboard_callback(callback: CallbackQuery, session: AsyncSession):
    await show_admin_panel(callback.message, session)
    await callback.answer()
