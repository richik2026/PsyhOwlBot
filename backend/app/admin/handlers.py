from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import create_admin, is_super_admin
from app.admin.referral_generator import build_referral_link
from app.referrals.service import create_referral_link

router = Router()


@router.message(Command("admin"))
async def admin_command(message: Message, db_session: AsyncSession):
    if not await is_super_admin(message.from_user.id):
        await message.answer("❌ У тебя нет прав для выполнения этой команды")
        return

    parts = message.text.split()

    if len(parts) < 2:
        await message.answer("Использование: /admin user_id")
        return

    user_id = int(parts[1])

    await create_admin(
        session=db_session,
        telegram_id=user_id,
    )

    referral_link = build_referral_link(user_id)

    await create_referral_link(
        session=db_session,
        admin_id=user_id,
        link=referral_link,
    )

    await message.answer("Администратор успешно добавлен 🦉")

    try:
        await message.bot.send_message(
            chat_id=user_id,
            text=(
                "Добро пожаловать в семью🦉\n\n"
                "Твоя персональная ссылка:\n\n"
                f"{referral_link}\n\n"
                "Все пользователи, которые придут по ней и оформят подписку, "
                "будут учитываться в твоей статистике 📈"
            ),
        )
    except Exception:
        pass
