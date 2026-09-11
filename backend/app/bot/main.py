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


async def check_telegram_network():
    try:
        addresses = await asyncio.to_thread(socket.getaddrinfo, "api.telegram.org", 443)
        logger.info("Telegram DNS OK: %s addresses", len(addresses))
    except Exception as e:
        logger.warning("Telegram DNS check failed: %s", e)


async def check_telegram_connection(bot: Bot):
    try:
        me = await bot.get_me()
        logger.info("Telegram API OK: @%s (%s)", me.username, me.id)
        return True
    except Exception as e:
        logger.exception("Telegram API check failed: %s", e)
        return False


async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is required")

    proxy = os.getenv("TELEGRAM_PROXY")

    if proxy:
        logger.info("Telegram session: proxy mode")
        session = AiohttpSession(proxy=proxy, timeout=90.0)
    else:
        logger.info("Telegram session: direct mode")
        session = AiohttpSession(timeout=90.0)

    await check_telegram_network()

    bot = Bot(
        token=token,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    logger.info("BOT STARTING. Token length: %s", len(token))
    await check_telegram_connection(bot)

    dp = Dispatcher()

    @dp.message()
    async def debug_all_messages(message):
        logger.info(
            "INCOMING MESSAGE user=%s text=%s",
            message.from_user.id if message.from_user else None,
            message.text,
        )

    dp.message.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())

    dp.include_router(router)

    scheduler_task = asyncio.create_task(daily_reports_loop(bot))

    try:
        logger.info("POLLING STARTED")
        await dp.start_polling(bot, polling_timeout=60)
    except Exception:
        logger.exception("Polling crashed")
        raise
    finally:
        scheduler_task.cancel()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
