from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(lambda message: message.text == "➕ Рилс")
async def add_reels_handler(message: Message):
    await message.answer(
        "Укажите количество рилсов которое вы выложили за сегодня"
    )
