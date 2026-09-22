from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.support.models import SupportMessage

router = Router()

SUPPORT_GROUP_ID = -1004387840594


@router.message(F.text == "🆘 Техподдержка")
async def support_handler(message: Message) -> None:
    await message.answer(
        "Напиши свой вопрос, и команда поддержки поможет тебе 🦉"
    )


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
