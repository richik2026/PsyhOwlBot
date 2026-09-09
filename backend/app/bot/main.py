import asyncio
import logging
import os
import socket

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from app.bot.router import router
from app.bot.middlewares.database import DatabaseMiddleware
from app.scheduler.service import daily_reports_loop


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IPv4AiohttpSession(AiohttpSession):
    """Aiogram HTTP session that forces direct Telegram traffic through IPv4."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # AiohttpSession builds its TCPConnector lazily from this config.
        # Passing connector=... to AiohttpSession is invalid: that kwarg is
        # forwarded to BaseSession and causes an "unexpected keyword" error.
        self._connector_init["family"] = socket.AF_INET


async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is required")

    proxy = os.getenv("TELEGRAM_PROXY", "").strip() or None

    # Variant 1: direct Telegram connection, forced to IPv4.
    # Variant 2: if TELEGRAM_PROXY is configured in Timeweb, use that proxy.
    if proxy:
        logger.info("Telegram connection mode: proxy")
        session = AiohttpSession(proxy=proxy, timeout=90.0)
    else:
        logger.info("Telegram connection mode: direct IPv4")
        session = IPv4AiohttpSession(timeout=90.0)

    logger.info("Telegram connection check. Token length: %s", len(token))

    bot = Bot(
        token=token,
        session=session,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    try:
        me = await bot.get_me()
        logger.info("Telegram connected successfully: @%s (id=%s)", me.username, me.id)
    except Exception as e:
        logger.exception(
            "Telegram connection failed. mode=%s error=%s",
            "proxy" if proxy else "direct IPv4",
            e,
        )
        raise

    dp = Dispatcher()

    db_middleware = DatabaseMiddleware()
    dp.message.middleware(db_middleware)
    dp.callback_query.middleware(db_middleware)

    dp.include_router(router)

    scheduler_task = asyncio.create_task(daily_reports_loop(bot))

    try:
        await dp.start_polling(
            bot,
            polling_timeout=60
        )
    finally:
        scheduler_task.cancel()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
