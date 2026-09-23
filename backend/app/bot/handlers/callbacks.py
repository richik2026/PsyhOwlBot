from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.dashboard import format_admin_dashboard, get_admin_dashboard
from app.admins.service import get_admin_by_telegram_id
from app.bot.keyboards.main import main_menu
from app.bot.states.reels import ReelsStates
from app.support.models import SupportMessage

router = Router()


@router.callback_query(F.data.startswith("support_claim:"))
async def support_claim_callback(callback: CallbackQuery, session: AsyncSession):
    admin = await get_admin_by_telegram_id(session, callback.from_user.id)

    if admin is None or not admin.is_active or admin.role not in {"ADMIN", "SUPER_ADMIN"}:
        await callback.answer("Только администраторы могут брать обращения", show_alert=True)
        return

    message_id = int(callback.data.split(":")[1])
    result = await session.execute(
        select(SupportMessage).where(SupportMessage.support_message_id == message_id)
    )
    request = result.scalar_one_or_none()

    if request is None:
        await callback.answer("Обращение не найдено", show_alert=True)
        return

    if request.admin_id:
        existing_admin = await get_admin_by_telegram_id(session, request.admin_id)
        username = existing_admin.username if existing_admin and existing_admin.username else str(request.admin_id)
        await callback.answer(
            f"Это обращение уже в обработке администратором @{username}",
            show_alert=True,
        )
        return

    request.admin_id = callback.from_user.id
    await session.commit()

    username = callback.from_user.username or str(callback.from_user.id)
    new_text = callback.message.html_text or callback.message.text or ""
    new_text += f"\n\n👤 <i>Взято в обработку админом @{username}</i>"

    await callback.message.edit_text(
        new_text,
        parse_mode="HTML",
        reply_markup=None,
    )
    await callback.answer()


@router.callback_query(F.data == "support")
async def support_callback(callback: CallbackQuery, state: FSMContext):
    from app.bot.handlers.support import send_support_prompt
    await send_support_prompt(callback.message, state)
    await callback.answer()


@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery, session: AsyncSession):
    admin = await get_admin_by_telegram_id(session, callback.from_user.id)
    is_admin = bool(admin and admin.is_active and admin.role in {"ADMIN", "SUPER_ADMIN"})

    await callback.message.answer(
        "🦉 Главное меню",
        reply_markup=main_menu(is_admin=is_admin, has_subscription=is_admin),
    )
    await callback.answer()


@router.callback_query(F.data == "talk")
async def talk_callback(callback: CallbackQuery):
    await callback.message.answer("Я рядом 🦉\n\nРасскажи, что сейчас происходит. О чём хочешь поговорить?")
    await callback.answer()


@router.callback_query(F.data == "admin_panel")
async def admin_panel_callback(callback: CallbackQuery, session: AsyncSession):
    admin = await get_admin_by_telegram_id(session, callback.from_user.id)
    if admin is None or not admin.is_active or admin.role not in {"ADMIN", "SUPER_ADMIN"}:
        await callback.message.answer("Эта команда доступна только администраторам")
        await callback.answer()
        return

    data = await get_admin_dashboard(session, admin)
    await callback.message.answer(format_admin_dashboard(data), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "add_reels")
async def add_reels_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ReelsStates.waiting_for_amount)
    await callback.message.answer(
        "📒 <b>Напиши количество рилсов которое ты опубликовал за сегодня</b>",
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "about_project")
async def about_project_callback(callback: CallbackQuery):
    await callback.message.answer("Раздел находится в разработке 🦉")
    await callback.answer()


@router.callback_query(F.data == "about_psychologists")
async def about_psychologists_callback(callback: CallbackQuery):
    await callback.message.answer("Раздел находится в разработке 🦉")
    await callback.answer()
