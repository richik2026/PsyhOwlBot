from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.dashboard import format_admin_dashboard, get_admin_dashboard
from app.admins.service import get_admin_by_telegram_id

router = Router()


@router.callback_query(F.data == "talk")
async def talk_callback(callback: CallbackQuery):
    await callback.message.answer(
        "Я рядом 🦉\n\n"
        "Расскажи, что сейчас происходит. О чём хочешь поговорить?"
    )
    await callback.answer()


@router.callback_query(F.data == "support")
async def support_callback(callback: CallbackQuery):
    await callback.message.answer(
        "Напиши свой вопрос, и команда поддержки поможет тебе 🦉"
    )
    await callback.answer()


@router.callback_query(F.data == "admin_panel")
async def admin_panel_callback(callback: CallbackQuery, session: AsyncSession):
    admin = await get_admin_by_telegram_id(session, callback.from_user.id)

    if admin is None or not admin.is_active:
        await callback.message.answer("Эта команда доступна только администраторам")
        await callback.answer()
        return

    data = await get_admin_dashboard(session, admin)
    await callback.message.answer(format_admin_dashboard(data), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "about_project")
async def about_project_callback(callback: CallbackQuery):
    await callback.message.answer("Раздел находится в разработке 🦉")
    await callback.answer()


@router.callback_query(F.data == "about_psychologists")
async def about_psychologists_callback(callback: CallbackQuery):
    await callback.message.answer("Раздел находится в разработке 🦉")
    await callback.answer()
