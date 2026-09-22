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
    try:
        addresses = await asyncio.to_thread(
            socket.getaddrinfo,
            "api.telegram.org",
            443
        )

        logger.info(
            "Telegram DNS OK: %s addresses",
            len(addresses)
        )

        for address in addresses:
            logger.info(
                "Telegram address: %s",
                address[4][0]
            )

    except Exception as e:
        logger.warning(
            "Telegram DNS check failed: %s",
            e
        )


async def check_telegram_connection(bot: Bot):
    try:
        me = await bot.get_me()

        logger.info(
            "Telegram API OK: @%s (%s)",
            me.username,
            me.id
        )

        return True

    except Exception as e:
        logger.exception(
            "Telegram API check failed: %s",
            e
        )

        return False


async def main() -> None:
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise RuntimeError(
            "BOT_TOKEN environment variable is required"
        )


    proxy = os.getenv("TELEGRAM_PROXY")


    # Принудительно используем IPv6,
    # так как IPv4 маршрут до Telegram на сервере таймаутится
    connector = aiohttp.TCPConnector(
        family=socket.AF_INET6,
        ttl_dns_cache=300
    )


    if proxy:
        session = AiohttpSession(
            proxy=proxy,
            timeout=90.0,
            connector=connector
        )
    else:
        session = AiohttpSession(
            timeout=90.0,
            connector=connector
        )


    await check_telegram_network()


    bot = Bot(
        token=token,
        session=session,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        ),
    )


    logger.info(
        "BOT STARTING. Token length: %s",
        len(token)
    )


    connected = await check_telegram_connection(bot)

    if not connected:
        logger.warning(
            "Telegram connection failed, starting polling anyway"
        )


    dp = Dispatcher()


    dp.message.middleware(
        DatabaseMiddleware()
    )

    dp.callback_query.middleware(
        DatabaseMiddleware()
    )


    dp.include_router(router)


    scheduler_task = asyncio.create_task(
        daily_reports_loop(bot)
    )


    try:
        logger.info(
            "POLLING STARTED"
        )

        await dp.start_polling(
            bot,
            polling_timeout=60
        )


    except Exception:
        logger.exception(
            "Polling crashed"
        )

        raise


    finally:

        scheduler_task.cancel()

        try:
            await scheduler_task
        except asyncio.CancelledError:
            pass


        await bot.session.close()



if __name__ == "__main__":
    asyncio.run(main())
