from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Рад тебя видеть у себя в гостях, о чём хочешь поговорить?"
    )
