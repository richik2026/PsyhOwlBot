import asyncio
import logging
import os
import socket

import aiohttp

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from app.bot.router import router
from app.bot.middlewares.database import DatabaseMiddleware
from app.scheduler.service import daily_reports_loop


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def check_telegram_network():
    """Diagnostic check: verify DNS, TCP and HTTPS access to Telegram."""
    try:
        addresses = await asyncio.to_thread(socket.getaddrinfo, "api.telegram.org", 443)
        logger.info("Telegram DNS resolved: %s addresses", len(addresses))
    except Exception as e:
        logger.error("Telegram network diagnostic failed: %s", e)


async def connect_telegram(bot: Bot):
    attempt = 0
    while True:
        try:
            me = await bot.get_me()
            logger.info("Telegram connected successfully: @%s (id=%s)", me.username, me.id)
            return
        except Exception as e:
            attempt += 1
            logger.warning(
                "Telegram connection attempt %s failed (%s). Retry in 10 seconds...",
                attempt,
                e,
            )
            await asyncio.sleep(10)


async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is required")

    proxy = os.getenv("TELEGRAM_PROXY")

    if proxy:
        logger.info("Telegram API mode: SOCKS5 proxy enabled")
        session = AiohttpSession(proxy=proxy, timeout=90.0)
    else:
        logger.info("Telegram API mode: direct aiogram session")
        session = AiohttpSession(timeout=90.0)

    await check_telegram_network()

    bot = Bot(
        token=token,
        session=session,
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
