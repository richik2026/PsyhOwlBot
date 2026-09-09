import asyncio
import logging
import os
import socket

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramNetworkError

from app.bot.router import router
from app.bot.middlewares.database import DatabaseMiddleware
from app.scheduler.service import daily_reports_loop


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResilientAiohttpSession(AiohttpSession):
    """Aiogram session with IPv4 forcing, retries and optional proxy failover."""

    def __init__(
        self,
        *,
        proxy: str | None = None,
        fallback_proxy: str | None = None,
        force_ipv4: bool = False,
        **kwargs,
    ):
        super().__init__(proxy=proxy, **kwargs)
        self._fallback_proxy = fallback_proxy if fallback_proxy != proxy else None
        self._using_fallback = False

        # AiohttpSession creates TCPConnector lazily. Passing connector=...
        # into AiohttpSession is invalid because it is forwarded to BaseSession.
        if force_ipv4 and proxy is None:
            self._connector_init["family"] = socket.AF_INET

    async def make_request(self, bot, method, timeout=None):
        last_error: TelegramNetworkError | None = None

        for attempt in range(1, 4):
            try:
                return await super().make_request(bot, method, timeout=timeout)
            except TelegramNetworkError as exc:
                last_error = exc
                logger.warning(
                    "Telegram network request failed (attempt %s/3, fallback=%s): %s",
                    attempt,
                    self._using_fallback,
                    exc,
                )

                # Drop the failed connection so the next attempt gets a fresh
                # socket/circuit rather than reusing a broken transport.
                await self.close()

                # One failed direct request is enough to switch to the local
                # fallback route when it is available. This is specifically for
                # Timeweb/RU-hosting routes where api.telegram.org may time out.
                if (
                    attempt == 1
                    and self._fallback_proxy
                    and not self._using_fallback
                ):
                    logger.warning(
                        "Switching Telegram transport to fallback SOCKS5 proxy."
                    )
                    self.proxy = self._fallback_proxy
                    self._using_fallback = True

                if attempt < 3:
                    await asyncio.sleep(attempt)

        assert last_error is not None
        raise last_error


async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is required")

    proxy = os.getenv("TELEGRAM_PROXY", "").strip() or None
    fallback_proxy = os.getenv("TELEGRAM_FALLBACK_PROXY", "").strip() or None

    if proxy:
        logger.info("Telegram connection mode: configured proxy")
        session = ResilientAiohttpSession(
            proxy=proxy,
            fallback_proxy=fallback_proxy,
            timeout=15.0,
        )
    else:
        logger.info(
            "Telegram connection mode: direct IPv4%s",
            " + fallback proxy" if fallback_proxy else "",
        )
        session = ResilientAiohttpSession(
            fallback_proxy=fallback_proxy,
            force_ipv4=True,
            timeout=15.0,
        )

    logger.info("Telegram connection check. Token length: %s", len(token))

    bot = Bot(
        token=token,
        session=session,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        ),
    )

    try:
        me = await bot.get_me()
        logger.info("Telegram connected successfully: @%s (id=%s)", me.username, me.id)
    except Exception as e:
        logger.exception("Telegram connection failed after retries: %s", e)
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
            polling_timeout=60,
        )
    finally:
        scheduler_task.cancel()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
