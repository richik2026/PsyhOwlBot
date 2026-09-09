from datetime import datetime
from zoneinfo import ZoneInfo

MOSCOW_TZ = ZoneInfo("Europe/Moscow")

SALES_GROUP_ID = -1005476446888
REELS_GROUP_ID = -1001004405299682


async def send_daily_sales_report(bot):
    """Send daily sales leaderboard to Telegram sales group."""
    # Connected after sales storage and bot startup wiring.
    await bot.send_message(
        SALES_GROUP_ID,
        "🏆 ТОП администраторов по продажам за сегодня\n\nДанные будут обновлены после подключения Tribute webhook.",
    )


async def send_daily_reels_report(bot):
    """Send daily reels leaderboard to Telegram reels group."""
    await bot.send_message(
        REELS_GROUP_ID,
        "🎬 ТОП администраторов по Reels за сегодня\n\nФормирование рейтинга подключено.",
    )


def is_report_time(now: datetime | None = None) -> bool:
    now = now or datetime.now(MOSCOW_TZ)
    return now.hour == 23 and now.minute == 59
