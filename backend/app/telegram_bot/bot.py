from aiogram import Bot, Dispatcher

from app.core.config import settings
from app.telegram_bot.handlers import start, menu, subscription


bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


def setup_routers():
    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(subscription.router)


async def start_bot():
    setup_routers()
    return dp
