from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def admin_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить рилсы", callback_data="add_reels")],
            [InlineKeyboardButton(text="🔗 Моя реферальная ссылка", callback_data="my_referral")],
        ]
    )
