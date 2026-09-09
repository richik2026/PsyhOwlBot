from aiogram import Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.dashboard import get_admin_dashboard, format_admin_dashboard
from app.admins.service import get_admin_by_telegram_id
from app.bot.keyboards.admin import admin_menu

router = Router()


@router.message(lambda message: message.text == "📊 Админ-Панель")
async def admin_dashboard(message: Message, session: AsyncSession):
    admin = await get_admin_by_telegram_id(session, message.from_user.id)

    if admin is None or not admin.is_active:
        await message.answer("Доступ только для администраторов")
        return

    data = await get_admin_dashboard(session, admin)
    await message.answer(
        format_admin_dashboard(data),
        reply_markup=admin_menu(),
    )
