import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.bot.router import router
from app.bot.middlewares.database import DatabaseMiddleware


async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is required")

    bot = Bot(token=token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    db_middleware = DatabaseMiddleware()
    dp.message.middleware(db_middleware)
    dp.callback_query.middleware(db_middleware)

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
