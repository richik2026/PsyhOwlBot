from app.telegram_bot.config import TRIBUTE_SUBSCRIPTION_URL


def subscription_button():
    return {
        "text": "💳 Подписка",
        "url": TRIBUTE_SUBSCRIPTION_URL,
    }


MAIN_MENU = [
    "🦉 О проекте",
    "🎙 Начать разговор",
    subscription_button(),
    "🆘 Техподдержка",
]
