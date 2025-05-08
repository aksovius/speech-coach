from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from shared.services.question_manager import set_user_question
from shared.services.question_service import get_question_for_user

router = Router()


@router.message(Command("question"))
async def handle_question(message: Message, **kwargs):
    db_session = kwargs.get("db")
    user_id = kwargs.get("user_id")

    # Получаем category из аргументов команды, если они есть
    command_args = message.text.split()
    category = command_args[1] if len(command_args) > 1 else None
    question = await get_question_for_user(user_id, db_session, category)
    set_user_question(message.from_user.id, question)
    await message.answer(
        f"<b>❓Question: 45 sec</b>\n{question.text}", parse_mode="HTML"
    )
