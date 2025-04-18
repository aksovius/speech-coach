# from audio.convert import convert_ogg_to_wav
# from whisper.transcribe import transcribe_audio
# from gpt.gpt_service import evaluate_answer
from aiogram import F, Router
from aiogram.types import Message
from services import audio_service
from services.question_manager import get_user_question

from config import settings

router = Router()


@router.message(F.voice)
async def handle_voice(message: Message, **kwargs):
    print("🔊 Обработка голосового сообщения")
    db_session = kwargs.get("db")
    user_id = kwargs.get("user_id")
    telegram_id = message.from_user.id
    question = get_user_question(telegram_id)
    if not question:
        await message.answer("🤖 Сначала попроси вопрос с помощью команды /question.")
        return

    try:
        print("📥 Голосовое сообщение получено")
        await message.answer("🤖 Обрабатываю ваше голосовое сообщение...")
        file_info = await message.bot.get_file(message.voice.file_id)
        file_url = f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{file_info.file_path}"
        result = await audio_service.process_voice_message(
            file_url, question, user_id, db_session
        )
        if result.get("error"):
            await message.answer(result.get("error"))
            return
        if result.get("transcription"):
            await message.answer(f"User: {result.get('transcription')}")
        if result.get("answer"):
            await message.answer(f"Coach: {result.get('answer')}")
    except Exception as e:
        print(f"❌ Ошибка обработки голосового сообщения: {e}")
        await message.answer(
            "❌ Произошла ошибка при обработке вашего голосового сообщения."
        )
