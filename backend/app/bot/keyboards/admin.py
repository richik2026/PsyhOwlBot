from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def admin_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Админ-Панель")],
            [KeyboardButton(text="➕ Рилс")],
        ],
        resize_keyboard=True,
    )
