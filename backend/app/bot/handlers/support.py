from aiogram import Router, F
from aiogram.types import Message

router = Router()

SUPPORT_GROUP_ID = -1004387840594


@router.message(F.text == "🆘 Техподдержка")
async def support_handler(message: Message) -> None:
    await message.answer(
        "Напиши свой вопрос, и команда поддержки поможет тебе 🦉"
    )

    # TODO: add user ↔ support group relay with reply mapping
