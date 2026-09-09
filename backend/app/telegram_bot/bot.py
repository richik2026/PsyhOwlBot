from aiogram import Bot, Dispatcher

from app.core.config import settings
from app.telegram_bot.handlers import start, menu, subscription
from app.telegram_bot.middleware.database import DatabaseMiddleware
from app.database.session import AsyncSessionLocal
from app.admin.handlers import router as admin_router


bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


def setup_middlewares():
    middleware = DatabaseMiddleware(AsyncSessionLocal)
    dp.message.middleware(middleware)
    dp.callback_query.middleware(middleware)


def setup_routers():
    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(subscription.router)
    dp.include_router(admin_router)


async def start_bot():
    setup_middlewares()
    setup_routers()
    return dp
