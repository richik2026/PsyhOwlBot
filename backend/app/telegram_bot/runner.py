import asyncio

from app.telegram_bot.bot import bot, dp, start_bot


async def main():
    await start_bot()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
