from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def main_menu(message: Message):
    await message.answer(
        "🦉 О проекте\n\n🎙 Начать разговор\n💳 Подписка\n🆘 Техподдержка"
    )
