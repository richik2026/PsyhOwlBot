from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.service import appoint_admin
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

        await message.answer("Администратор назначен и ссылка отправлена 🦉")

    except PermissionError:
        await message.answer("Недостаточно прав")
    except Exception as exc:
        await message.answer(f"Ошибка назначения администратора: {exc}")
