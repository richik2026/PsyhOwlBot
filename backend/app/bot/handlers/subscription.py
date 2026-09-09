from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

router = Router()

TRIBUTE_URL = "https://t.me/tribute/app?startapp=s12Ac"


@router.message(F.text == "💳 Подписка")
async def subscription_handler(message: Message) -> None:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Оформить подписку", url=TRIBUTE_URL)]
        ]
    )
    await message.answer(
        "Подписка открывает 60 часов разговоров с Кришем на 30 дней. "
        "Дневной лимит — до 2 часов.",
        reply_markup=keyboard,
    )
