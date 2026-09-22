from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu(is_admin: bool = False) -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="🦉 О проекте")],
        [KeyboardButton(text="🎙 Начать разговор")],
        [KeyboardButton(text="💳 Подписка")],
        [KeyboardButton(text="🆘 Техподдержка")],
    ]

    if is_admin:
        buttons.append([KeyboardButton(text="🦉 Админ-Панель")])

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
    )
