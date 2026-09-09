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


class DualStackAiohttpSession(AiohttpSession):
    """Aiogram HTTP session that allows both IPv4 and IPv6 for Telegram."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Do not force IPv4. Let aiohttp use the address family that works on
        # the hosting provider. This can use IPv6 when the IPv4 route to
        # api.telegram.org is unreliable.
        self._connector_init["family"] = socket.AF_UNSPEC


async def connect_telegram(bot: Bot, mode: str):
    """Keep trying Telegram connection when the hosting provider drops traffic."""
    attempt = 0
    while True:
        try:
            me = await bot.get_me()
            logger.info(
                "Telegram connected successfully: @%s (id=%s)",
                me.username,
                me.id,
            )
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

    proxy = os.getenv("TELEGRAM_PROXY", "").strip() or None

    if proxy:
        logger.info("Telegram connection mode: configured proxy")
        session = AiohttpSession(proxy=proxy, timeout=90.0)
    else:
        logger.info("Telegram connection mode: dual-stack IPv4/IPv6")
        session = DualStackAiohttpSession(timeout=90.0)

    logger.info("Telegram connection check. Token length: %s", len(token))

    bot = Bot(
        token=token,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await connect_telegram(bot, "proxy" if proxy else "dual-stack")

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
