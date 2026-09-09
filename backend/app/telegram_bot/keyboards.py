from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.telegram_bot.config import TRIBUTE_SUBSCRIPTION_URL


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🦉 О проекте", callback_data="about")],
            [InlineKeyboardButton(text="🎙 Начать разговор", callback_data="start_conversation")],
            [InlineKeyboardButton(text="💳 Подписка", url=TRIBUTE_SUBSCRIPTION_URL)],
            [InlineKeyboardButton(text="🆘 Техподдержка", callback_data="support")],
        ]
    )
