import asyncio
import logging
import os
import socket

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode

from app.bot.router import router
from app.bot.middlewares.database import DatabaseMiddleware
from app.scheduler.service import daily_reports_loop


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DualStackAiohttpSession(AiohttpSession):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._connector_init["family"] = socket.AF_UNSPEC


async def connect_telegram(bot: Bot):
    attempt = 0
    while True:
        try:
            me = await bot.get_me()
            logger.info("Telegram connected successfully: @%s (id=%s)", me.username, me.id)
            return
        except Exception as e:
            attempt += 1
            logger.warning("Telegram connection attempt %s failed (%s). Retry in 10 seconds...", attempt, e)
            await asyncio.sleep(10)


async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is required")

    local_api = os.getenv("TELEGRAM_LOCAL_API", "http://telegram-bot-api:8081")
    server = TelegramAPIServer.from_base(local_api)

    logger.info("Telegram API mode: local server %s", local_api)

    session = DualStackAiohttpSession(timeout=90.0)

    bot = Bot(
        token=token,
        session=session,
        server=server,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    logger.info("Telegram connection check. Token length: %s", len(token))
    await connect_telegram(bot)

    dp = Dispatcher()

    db_middleware = DatabaseMiddleware()
    dp.message.middleware(db_middleware)
    dp.callback_query.middleware(db_middleware)

    dp.include_router(router)

    scheduler_task = asyncio.create_task(daily_reports_loop(bot))

    try:
        await dp.start_polling(bot, polling_timeout=60)
    finally:
        scheduler_task.cancel()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
