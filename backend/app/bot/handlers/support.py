from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.support.models import SupportMessage

router = Router()

SUPPORT_GROUP_ID = -1004387840594


@router.message(F.text == "🆘 Техподдержка")
async def support_handler(message: Message) -> None:
    await message.answer(
        "Напиши свой вопрос, и команда поддержки поможет тебе 🦉"
    )


@router.message(F.reply_to_message)
async def support_reply_handler(message: Message, session: AsyncSession) -> None:
    if message.chat.id != SUPPORT_GROUP_ID:
        return

    replied_message = message.reply_to_message

    result = await session.execute(
        select(SupportMessage).where(
            SupportMessage.support_message_id == replied_message.message_id
        )
    )
    support_request = result.scalar_one_or_none()

    if support_request is None:
        return

    await message.bot.send_message(
        support_request.user_id,
        f"🦉 Ответ поддержки:\n\n{message.text or 'Получено сообщение от поддержки'}",
    )

    support_request.admin_id = message.from_user.id
    await session.commit()


@router.message()
async def support_relay(message: Message, session: AsyncSession) -> None:
    if not message.text:
        return

    if message.chat.id == SUPPORT_GROUP_ID:
        return

    sent = await message.bot.send_message(
        SUPPORT_GROUP_ID,
        f"🆘 Запрос поддержки\n\n"
        f"Пользователь: {message.from_user.full_name}\n"
        f"ID: {message.from_user.id}\n\n"
        f"{message.text}",
    )

    session.add(
        SupportMessage(
            user_id=message.from_user.id,
            support_message_id=sent.message_id,
        )
    )
    await session.commit()
