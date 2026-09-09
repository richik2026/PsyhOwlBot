from aiogram import Bot, Dispatcher

from app.core.config import settings
from app.telegram_bot.handlers import start


bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


def setup_routers():
    dp.include_router(start.router)


async def start_bot():
    setup_routers()
    return dp
