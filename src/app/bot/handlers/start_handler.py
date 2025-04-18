from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("👋 Привет! Я помогу тебе тренировать английский...")
