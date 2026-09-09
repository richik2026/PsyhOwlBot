import asyncio

from app.telegram_bot.bot import bot, start_bot


async def main():
    await start_bot()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.start_polling(bot.dispatcher)


if __name__ == "__main__":
    asyncio.run(main())
