from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.dashboard import format_admin_dashboard, get_admin_dashboard
from app.admins.service import appoint_admin, get_admin_by_telegram_id
from app.referrals.service import build_referral_url, get_or_create_admin_referral

router = Router()


@router.message(Command("admin"))
async def admin_command(message: Message, session: AsyncSession):
    parts = message.text.split()

    if len(parts) != 2:
        await message.answer("Использование:\n/admin USER_ID")
        return

    try:
        target_id = int(parts[1])
    except ValueError:
        await message.answer("USER_ID должен быть числом")
        return

    try:
        admin = await appoint_admin(
            session,
            actor_telegram_id=message.from_user.id,
            target_telegram_id=target_id,
        )

        referral = await get_or_create_admin_referral(session, admin)
        bot_username = (await message.bot.get_me()).username
        link = build_referral_url(bot_username, referral.code)

        await message.bot.send_message(
            target_id,
            "Добро пожаловать в семью🦉\n\n"
            f"Твоя персональная ссылка:\n\n{link}\n\n"
            "Все пользователи, которые придут по ней и оформят подписку, "
            "будут учитываться в твоей статистике 📈",
        )

        await session.commit()
        await message.answer("Администратор назначен и ссылка отправлена 🦉")

    except PermissionError:
        await message.answer("Недостаточно прав")
    except Exception as exc:
        await message.answer(f"Ошибка назначения администратора: {exc}")


@router.message(Command("my_stats"))
async def my_stats(message: Message, session: AsyncSession):
    admin = await get_admin_by_telegram_id(session, message.from_user.id)

    if admin is None or not admin.is_active:
        await message.answer("Эта команда доступна только администраторам")
        return

    data = await get_admin_dashboard(session, admin)
    await message.answer(format_admin_dashboard(data))
