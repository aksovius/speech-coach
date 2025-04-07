from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from gpt.gpt_service import generate_question
from services.question_manager import set_user_question

router = Router()

@router.message(Command("question"))
async def handle_question(message: Message):
    question = await generate_question()
    set_user_question(message.from_user.id, question)
    await message.answer(f"❓ Вот вопрос для тебя:\n{question}")
