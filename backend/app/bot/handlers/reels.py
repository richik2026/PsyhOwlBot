from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.bot.states.reels import ReelsStates

router = Router()


@router.message(lambda message: message.text == "➕ Рилс")
async def add_reels_handler(message: Message, state: FSMContext):
    await state.set_state(ReelsStates.waiting_for_amount)
    await message.answer(
        "Укажите количество рилсов которое вы выложили за сегодня"
    )


@router.message(ReelsStates.waiting_for_amount)
async def save_reels_amount(message: Message, state: FSMContext):
    if not message.text or not message.text.isdigit():
        await message.answer("Введите количество рилсов числом")
        return

    amount = int(message.text)

    await state.clear()
    await message.answer(
        f"Количество рилсов за сегодня сохранено: {amount} 🎬"
    )
