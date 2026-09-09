from aiogram import Router, F
from aiogram.types import Message

from app.reels.service import add_reels

router = Router()


@router.message(F.text == "➕ Рилс")
async def request_reels_count(message: Message):
    await message.answer(
        "Укажите количество рилсов которое вы выложили за сегодня"
    )


@router.message(F.text.regexp(r"^\d+$"))
async def save_reels_count(message: Message, session):
    await add_reels(
        session=session,
        admin_id=message.from_user.id,
        number_of_reels=int(message.text),
    )
    await session.commit()
    await message.answer("Количество рилсов сохранено ✅")
