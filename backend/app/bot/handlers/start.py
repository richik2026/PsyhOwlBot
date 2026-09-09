from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.bot.keyboards.main import main_menu

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Рад тебя видеть у Совёнка Криша 🦉\n\nО чём хочешь поговорить?",
        reply_markup=main_menu(),
    )
