from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(lambda message: message.text == "🎙 Начать разговор")
async def start_conversation(message: Message):
    await message.answer(
        "Я рядом 🦉\n\n"
        "Расскажи, что сейчас происходит. О чём хочешь поговорить?"
    )


@router.message(lambda message: message.text == "🦉 О проекте")
async def about_project(message: Message):
    await message.answer(
        "Я — Совёнок Криш 🦉\n\n"
        "Твой AI-компаньон для спокойного разговора и размышлений."
    )
