from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.service import get_admin_by_telegram_id
from app.bot.states.reels import ReelsStates
from app.reels.service import add_reels, get_reels_rating_today

router = Router()


@router.message(lambda message: message.text in {"➕ Рилс", "+ Рилс"})
async def add_reels_handler(message: Message, state: FSMContext):
    await state.set_state(ReelsStates.waiting_for_amount)
    await message.answer(
        "📒 <b>Напиши количество рилсов которое ты опубликовал за сегодня</b>",
        parse_mode="HTML",
    )


@router.message(ReelsStates.waiting_for_amount)
async def save_reels_amount(message: Message, state: FSMContext, session: AsyncSession):
    if not message.text or not message.text.isdigit():
        await message.answer("❗️УКАЖИТЕ ЦИФРУ!")
        return

    admin = await get_admin_by_telegram_id(session, message.from_user.id)
    if admin is None or not admin.is_active:
        await state.clear()
        await message.answer("Добавлять статистику могут только администраторы")
        return

    amount = int(message.text)
    await add_reels(session, admin.id, amount)
    await session.commit()

    rating = await get_reels_rating_today(session)
    place = None
    for index, item in enumerate(rating, start=1):
        if item.admin_id == admin.id:
            place = index
            break

    await state.clear()

    place_text = str(place) if place else "—"

    await message.answer(
        "👍 <b>Спасибо за работу, коллега!</b>\n\n"
        f"⚡ Теперь вы в топе <b>{place_text} место</b>",
        parse_mode="HTML",
    )
