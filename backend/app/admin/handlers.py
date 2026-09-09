from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import create_admin, is_super_admin

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

    await message.answer(
        "Администратор успешно добавлен 🦉"
    )

    try:
        await message.bot.send_message(
            chat_id=user_id,
            text=(
                "Добро пожаловать в семью🦉\n\n"
                "Твоя персональная ссылка:\n\n"
                "...\n\n"
                "Все пользователи, которые придут по ней и оформят подписку, "
                "будут учитываться в твоей статистике 📈"
            ),
        )
    except Exception:
        pass
