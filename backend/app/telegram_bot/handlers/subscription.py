from aiogram import Router
from aiogram.types import Message

from app.telegram_bot.config import TRIBUTE_SUBSCRIPTION_URL

router = Router()


@router.message(lambda message: message.text == "💳 Подписка")
async def subscription_handler(message: Message):
    await message.answer(
        f"Оформить доступ к Кришу можно здесь:\n{TRIBUTE_SUBSCRIPTION_URL}"
    )
