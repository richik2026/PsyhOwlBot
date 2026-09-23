from html import escape

from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.support.models import SupportMessage

router = Router()

SUPPORT_GROUP_ID = -1004387840594


def support_claim_keyboard(message_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✏️ Взять в обработку", callback_data=f"support_claim:{message_id}")]
        ]
    )


async def send_support_prompt(message: Message):
    await message.answer(
        "✏️ <b>Техническая поддержка Совёнка</b>\n\n"
        "📨 Напиши интересующий тебя вопрос и наша команда\n"
        "ответит тебе в течении пары мгновений!\n\n"
        "🗒 Отвечаем очень быстро с 05:00 — 00:00",
        parse_mode="HTML",
    )


@router.message(F.text == "🆘 Техподдержка")
async def support_handler(message: Message) -> None:
    await send_support_prompt(message)


@router.message(F.text)
async def support_relay(message: Message, session: AsyncSession) -> None:
    if message.chat.id == SUPPORT_GROUP_ID:
        return

    text = (
        "❗️ <b>ВНИМАНИЕ, НОВОЕ ОБРАЩЕНИЕ!</b>\n\n"
        f"💔 <b>Пользователь:</b> @{escape(message.from_user.username or str(message.from_user.id))}\n\n"
        f"💬 <b>Сообщение:</b>\n{escape(message.text)}"
    )

    sent = await message.bot.send_message(
        SUPPORT_GROUP_ID,
        text,
        parse_mode="HTML",
        reply_markup=support_claim_keyboard(0),
    )

    await message.bot.edit_message_reply_markup(
        chat_id=SUPPORT_GROUP_ID,
        message_id=sent.message_id,
        reply_markup=support_claim_keyboard(sent.message_id),
    )

    session.add(
        SupportMessage(
            user_id=message.from_user.id,
            support_message_id=sent.message_id,
        )
    )
    await session.commit()


@router.message(F.reply_to_message)
async def support_reply_handler(message: Message, session: AsyncSession) -> None:
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
        f"🦉 <b>Ответ поддержки:</b>\n\n{escape(message.text or 'Получено сообщение от поддержки')}",
        parse_mode="HTML",
    )

    support_request.admin_id = message.from_user.id
    await session.commit()
