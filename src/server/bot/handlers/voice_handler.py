# from audio.convert import convert_ogg_to_wav
# from whisper.transcribe import transcribe_audio
# from gpt.gpt_service import evaluate_answer
from aiogram import F, Router
from aiogram.types import Message
from shared.config import settings
from shared.services import audio_service
from shared.services.question_manager import get_user_question

router = Router()


@router.message(F.voice)
async def handle_voice(message: Message, **kwargs):
    print("📥 Голосовое сообщение получено")
    user_id = kwargs.get("user_id")
    telegram_id = message.from_user.id
    question = get_user_question(telegram_id)
    if not question:
        await message.answer("🤖 Ask question first /question.")
        return

    try:

        await message.answer("🤖 Processing your voice message...")
        file_info = await message.bot.get_file(message.voice.file_id)
        file_url = f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{file_info.file_path}"
        await audio_service.process_voice_message(file_url, user_id, telegram_id)
    except Exception as e:
        print(f"❌ Ошибка обработки голосового сообщения: {e}")
        await message.answer(
            "❌ An error occurred while processing your voice message."
        )
