from html import escape

from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.service import get_admin_by_telegram_id
from app.support.models import SupportMessage

router = Router()

SUPPORT_GROUP_ID = -1004387840594


class SupportStates(StatesGroup):
    waiting_message = State()


def support_claim_keyboard(message_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="💬 Ответить", callback_data=f"support_claim:{message_id}")]])


def back_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="↩️ В главное меню", callback_data="main_menu")]])


async def send_support_prompt(message: Message, state: FSMContext):
    await state.set_state(SupportStates.waiting_message)
    await message.answer(
        "📨 <b>Техническая поддержка Совёнка</b>\n\n"
        "Напиши свой вопрос одним сообщением.",
        parse_mode="HTML"
    )


@router.message(F.text == "🆘 Техподдержка")
async def support_handler(message: Message, state: FSMContext):
    await send_support_prompt(message, state)


@router.callback_query(F.data == "support")
async def support_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await send_support_prompt(callback.message, state)


@router.message(SupportStates.waiting_message, F.text)
async def support_relay(message: Message, state: FSMContext, session: AsyncSession):
    sent = await message.bot.send_message(
        SUPPORT_GROUP_ID,
        "❗️ <b>НОВОЕ ОБРАЩЕНИЕ</b>\n\n"
        f"👤 Пользователь: @{escape(message.from_user.username or str(message.from_user.id))}\n\n"
        f"💬 Сообщение:\n{escape(message.text)}",
        parse_mode="HTML"
    )

    await sent.edit_reply_markup(reply_markup=support_claim_keyboard(sent.message_id))

    session.add(SupportMessage(
        user_id=message.from_user.id,
        support_message_id=sent.message_id,
        status="new"
    ))
    await session.commit()
    await state.clear()

    await message.answer(
        "✅ Благодарим за обращение, на него ответят в ближайшее время.",
        reply_markup=back_menu_keyboard()
    )


@router.callback_query(F.data.startswith("support_claim:"))
async def support_claim(callback: CallbackQuery, session: AsyncSession):
    admin = await get_admin_by_telegram_id(session, callback.from_user.id)
    if not admin or admin.role not in {"ADMIN", "SUPER_ADMIN"}:
        await callback.answer("Недостаточно прав", show_alert=True)
        return

    message_id = int(callback.data.split(":", 1)[1])
    result = await session.execute(select(SupportMessage).where(SupportMessage.support_message_id == message_id))
    ticket = result.scalar_one_or_none()

    if not ticket:
        await callback.answer("Обращение не найдено", show_alert=True)
        return

    if ticket.admin_id:
        await callback.answer("⚠️ Это обращение уже взял в обработку админ", show_alert=True)
        return

    ticket.admin_id = callback.from_user.id
    ticket.status = "processing"
    await session.commit()

    username = callback.from_user.username or str(callback.from_user.id)
    await callback.message.edit_text(
        callback.message.html_text + "\n\n✅ <b>Взято в работу</b>\nАдминистратор: @" + escape(username),
        parse_mode="HTML",
        reply_markup=None
    )

    await callback.answer("Напишите ответ следующим сообщением в группе")


@router.message(F.chat.id == SUPPORT_GROUP_ID, F.text)
async def admin_support_answer(message: Message, session: AsyncSession):
    admin = await get_admin_by_telegram_id(session, message.from_user.id)
    if not admin:
        return

    result = await session.execute(select(SupportMessage).where(
        SupportMessage.admin_id == message.from_user.id,
        SupportMessage.status == "processing"
    ).order_by(SupportMessage.created_at.desc()))

    ticket = result.scalars().first()
    if not ticket:
        return

    await message.bot.send_message(
        ticket.user_id,
        "💬 <b>Ответ поддержки:</b>\n\n" + escape(message.text),
        parse_mode="HTML"
    )

    ticket.status = "answered"
    await session.commit()
