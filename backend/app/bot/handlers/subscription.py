from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

router = Router()

TRIBUTE_URL = "https://t.me/tribute/app?startapp=s12Ac"


@router.message(F.text == "💳 Подписка")
async def subscription_handler(message: Message) -> None:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🤍 Активировать подписку", url=TRIBUTE_URL)]
        ]
    )
    await message.answer(
        "🤍 Открой доступ к 60 часам разговоров с Кришем на целый месяц!"
        "🦉 Общайся с настоящим психологическим другом обученным на материалах лучших мировых университетов и не переплачивай деньги психологам!",
        reply_markup=keyboard,
    )
