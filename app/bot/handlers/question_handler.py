from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from services.question_manager import set_user_question
from services.question_service import get_question_for_user
router = Router()

@router.message(Command("question"))
async def handle_question(message: Message):
    question = await get_question_for_user(message.from_user)
    set_user_question(message.from_user.id, question)
    await message.answer(f"❓ Вот вопрос для тебя:\n{question}")
