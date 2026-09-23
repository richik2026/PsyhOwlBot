from html import escape

from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.support.models import SupportMessage

router = Router()

SUPPORT_GROUP_ID = -1004387840594


class SupportStates(StatesGroup):
    waiting_message = State()


def support_claim_keyboard(message_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text="✏️ Взять в обработку",
            callback_data=f"support_claim:{message_id}"
        )]]
    )


def back_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text="↩️ В главное меню",
            callback_data="main_menu"
        )]]
    )


async def send_support_prompt(message: Message, state: FSMContext):
    await state.set_state(SupportStates.waiting_message)
    await message.answer(
        "✏️ <b>Техническая поддержка Совёнка</b>\n\n"
        "📨 Напиши интересующий тебя вопрос и наша команда ответит тебе в течении пары мгновений!\n\n"
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

    sent = await message.bot.send_message(
        SUPPORT_GROUP_ID,
        text,
        parse_mode="HTML"
    )

    await message.bot.edit_message_reply_markup(
        SUPPORT_GROUP_ID,
        sent.message_id,
        reply_markup=support_claim_keyboard(sent.message_id)
    )

    session.add(
        SupportMessage(
            user_id=message.from_user.id,
            support_message_id=sent.message_id
        )
    )
    await session.commit()
    await state.clear()

    await message.answer(
        "❤️ Благодарим за обращение! ❤️",
        reply_markup=back_menu_keyboard()
    )


@router.message(F.reply_to_message)
async def support_reply_handler(message: Message, session: AsyncSession):
    if message.chat.id != SUPPORT_GROUP_ID:
        return

    result = await session.execute(
        SupportMessage.__table__.select().where(
            SupportMessage.support_message_id == message.reply_to_message.message_id
        )
    )
    support_request = result.scalar_one_or_none()

    if support_request is None:
        return

    await message.bot.send_message(
        support_request.user_id,
        f"🦉 <b>Ответ поддержки:</b>\n\n{escape(message.text or '')}",
        parse_mode="HTML"
    )
