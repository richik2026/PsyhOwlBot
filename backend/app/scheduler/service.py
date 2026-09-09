import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from app.scheduler.reports import send_daily_reels_report, send_daily_sales_report

MOSCOW_TZ = ZoneInfo("Europe/Moscow")


async def daily_reports_loop(bot):
    """Background loop for daily Telegram leaderboards."""
    sent_date = None

    while True:
        now = datetime.now(MOSCOW_TZ)

        if now.hour == 23 and now.minute == 59 and sent_date != now.date():
            await send_daily_sales_report(bot)
            await send_daily_reels_report(bot)
            sent_date = now.date()

        await asyncio.sleep(30)
