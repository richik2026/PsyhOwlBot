from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🦉 О проекте")],
            [KeyboardButton(text="🎙 Начать разговор")],
            [KeyboardButton(text="💳 Подписка")],
            [KeyboardButton(text="🆘 Техподдержка")],
        ],
        resize_keyboard=True,
    )
