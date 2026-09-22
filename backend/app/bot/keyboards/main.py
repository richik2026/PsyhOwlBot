from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu(is_admin: bool = False, has_subscription: bool = False) -> ReplyKeyboardMarkup:
    if not has_subscription and not is_admin:
        buttons = [
            [KeyboardButton(text="🏆 Купить подписку")],
            [KeyboardButton(text="💬 Чат с поддержкой")],
            [KeyboardButton(text="📕 Почему я круче людей психологов?")],
        ]
    elif is_admin:
        buttons = [
            [KeyboardButton(text="🦉 Поговорить с Совёнком")],
            [KeyboardButton(text="💬 Чат с поддержкой")],
            [KeyboardButton(text="💳 Продлить подписку")],
            [KeyboardButton(text="📕 Подробнее о нас")],
            [KeyboardButton(text="👑 Админ-панель")],
        ]
    else:
        buttons = [
            [KeyboardButton(text="🦉 Поговорить с Совёнком")],
            [KeyboardButton(text="💬 Чат с поддержкой")],
            [KeyboardButton(text="💳 Продлить подписку")],
            [KeyboardButton(text="📕 Подробнее о нас")],
        ]

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
    )
