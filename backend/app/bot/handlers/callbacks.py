from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.admin import open_admin_panel
from app.bot.states.reels import ReelsStates
from app.admins.service import get_admin_by_telegram_id
from app.referrals.service import get_or_create_admin_referral, build_referral_url

router = Router()


async def is_admin(session: AsyncSession, telegram_id: int, username: str | None = None):
    admin = await get_admin_by_telegram_id(session, telegram_id)
    return admin and admin.is_active


@router.callback_query(F.data == "admin_panel")
async def admin_panel_callback(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()

    await open_admin_panel(
        session,
        callback.from_user.id,
        callback.message.answer,
    )


@router.callback_query(F.data == "my_referral")
async def my_referral_callback(callback: CallbackQuery, session: AsyncSession):
    admin = await get_admin_by_telegram_id(session, callback.from_user.id)
    if admin is None or not admin.is_active:
        await callback.answer("Нет доступа", show_alert=True)
        return

    referral = await get_or_create_admin_referral(session, admin)
    bot_username = (await callback.bot.get_me()).username
    link = build_referral_url(bot_username, referral.code)
    await session.commit()

    await callback.message.answer(
        "🔗 <b>Твоя персональная реферальная ссылка:</b>\n\n"
        f"{link}\n\n"
        "Работай усерднее, чтобы как можно больше пользователей пришло по твоей ссылке, ведь в топе администраторов видно кто самый крутой инвайтер🦉",
        parse_mode="HTML",
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
