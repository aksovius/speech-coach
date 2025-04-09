from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def handle_start(message: Message):
    print(f"Received /start command from user: {message.from_user}")
    await message.answer("👋 Привет! Я помогу тебе тренировать английский...")
