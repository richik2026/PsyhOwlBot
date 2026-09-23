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
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text="✏️ Взять в обработку",
        callback_data=f"support_claim:{message_id}"
    )]])


def back_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text="↩️ В главное меню",
        callback_data="main_menu"
    )]])


async def send_support_prompt(message: Message, state: FSMContext):
    await state.set_state(SupportStates.waiting_message)
    await message.answer(
        "📨 <b>Техническая поддержка Совёнка</b>\n\n"
        "Напиши интересующий тебя вопрос и наша команда ответит тебе в течении пары мгновений!\n\n"
        "🗒 Отвечаем очень быстро с 05:00 — 00:00",
        parse_mode="HTML"
    )


@router.message(F.text == "🆘 Техподдержка")
async def support_handler(message: Message, state: FSMContext):
    await send_support_prompt(message, state)


@router.message(SupportStates.waiting_message, F.text)
async def support_relay(message: Message, state: FSMContext, session: AsyncSession):
    text = (
        "❗️ <b>ВНИМАНИЕ, НОВОЕ ОБРАЩЕНИЕ!</b>\n\n"
        f"💔 <b>Пользователь:</b> @{escape(message.from_user.username or str(message.from_user.id))}\n\n"
        f"💬 <b>Сообщение:</b>\n{escape(message.text)}"
    )

    sent = await message.bot.send_message(SUPPORT_GROUP_ID, text, parse_mode="HTML", reply_markup=support_claim_keyboard(0))
    await message.bot.edit_message_reply_markup(SUPPORT_GROUP_ID, sent.message_id, reply_markup=support_claim_keyboard(sent.message_id))

    session.add(SupportMessage(user_id=message.from_user.id, support_message_id=sent.message_id))
    await session.commit()
    await state.clear()

    await message.answer("❤️ Благодарим за обращение! ❤️", reply_markup=back_menu_keyboard())


@router.callback_query(F.data.startswith("support_claim:"))
async def support_claim(callback: CallbackQuery, session: AsyncSession):
    admin = await get_admin_by_telegram_id(session, callback.from_user.id)
    if not admin or admin.role not in {"ADMIN", "SUPER_ADMIN"}:
        await callback.answer("Недостаточно прав", show_alert=True)
        return

    message_id = int(callback.data.split(":")[1])
    result = await session.execute(select(SupportMessage).where(SupportMessage.support_message_id == message_id))
    request = result.scalar_one_or_none()

    if request is None:
        await callback.answer("Обращение не найдено", show_alert=True)
        return

    if request.admin_id:
        current = await session.execute(select(SupportMessage).where(SupportMessage.id == request.id))
        existing = current.scalar_one()
        await callback.answer("Это обращение уже в обработке администратором", show_alert=True)
        return

    request.admin_id = admin.id
    await session.commit()

    await callback.message.edit_text(
        callback.message.html_text + f"\n\n👤 <b>Взято в обработку админом @{escape(callback.from_user.username or str(callback.from_user.id))}</b>",
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(F.reply_to_message)
async def support_reply_handler(message: Message, session: AsyncSession):
    if message.chat.id != SUPPORT_GROUP_ID:
        return
    result = await session.execute(select(SupportMessage).where(SupportMessage.support_message_id == message.reply_to_message.message_id))
    support_request = result.scalar_one_or_none()
    if support_request is None:
        return
    await message.bot.send_message(support_request.user_id, f"🦉 <b>Ответ поддержки:</b>\n\n{escape(message.text or '')}", parse_mode="HTML")
