from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("admin"))
async def admin_command(message: Message):
    await message.answer(
        "Использование:\n/admin USER_ID"
    )
