from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

SUBSCRIPTION_URL = "https://t.me/tribute/app?startapp=s12Ac"


def main_menu(is_admin: bool = False, has_subscription: bool = False) -> InlineKeyboardMarkup:
    if not has_subscription and not is_admin:
        buttons = [
            [InlineKeyboardButton(text="🏆 Купить подписку", url=SUBSCRIPTION_URL)],
            [InlineKeyboardButton(text="💬 Чат с поддержкой", callback_data="support")],
            [InlineKeyboardButton(text="📕 Почему я круче психологов", callback_data="about_psychologists")],
        ]
    elif is_admin:
        buttons = [
            [InlineKeyboardButton(text="🦉 Поговорить с Совёнком", callback_data="talk")],
            [InlineKeyboardButton(text="💬 Чат с поддержкой", callback_data="support")],
            [InlineKeyboardButton(text="💳 Продлить подписку", url=SUBSCRIPTION_URL)],
            [InlineKeyboardButton(text="📕 Подробнее о нас", callback_data="about_project")],
            [InlineKeyboardButton(text="👑 Админ-панель", callback_data="admin_panel")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text="🦉 Поговорить с Совёнком", callback_data="talk")],
            [InlineKeyboardButton(text="💬 Чат с поддержкой", callback_data="support")],
            [InlineKeyboardButton(text="💳 Продлить подписку", url=SUBSCRIPTION_URL)],
            [InlineKeyboardButton(text="📕 Подробнее о нас", callback_data="about_project")],
        ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
