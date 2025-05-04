# from audio.convert import convert_ogg_to_wav
# from whisper.transcribe import transcribe_audio
# from gpt.gpt_service import evaluate_answer
import os

from aiogram import F, Router
from aiogram.types import Message

from shared.config import settings
from shared.logging import get_log_level, setup_logger
from shared.services import audio_service
from shared.services.question_manager import get_user_question

# Configure logger with Loki formatter
logger = setup_logger(
    name="server.bot.voice",
    level=get_log_level(os.getenv("LOG_LEVEL", "INFO")),
    service=os.getenv("LOG_SERVICE", "speech-coach"),
    component="server.bot.voice",
    use_loki=True,
)

router = Router()


@router.message(F.voice)
async def handle_voice(message: Message, **kwargs):
    logger.info(
        "Voice message received",
        extra={"event": "voice_received", "chat_id": message.chat.id},
    )
    user_id = kwargs.get("user_id")
    telegram_id = message.from_user.id
    question = get_user_question(telegram_id)
    if not question:
        logger.info(
            "No question found for user",
            extra={"event": "no_question", "telegram_id": telegram_id},
        )
        await message.answer("🤖 Ask question first /question.")
        return

    try:
        await message.answer("🤖 Processing your voice message...")
        file_info = await message.bot.get_file(message.voice.file_id)
        file_url = f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{file_info.file_path}"

        logger.info(
            "Processing voice message",
            extra={
                "event": "voice_processing",
                "telegram_id": telegram_id,
                "user_id": user_id,
                "voice_duration": message.voice.duration,
                "file_id": message.voice.file_id,
            },
        )

        await audio_service.process_voice_message(file_url, user_id, telegram_id)
    except Exception as e:
        logger.error(
            "Voice message processing error",
            extra={"event": "voice_error", "error": str(e), "telegram_id": telegram_id},
        )
        await message.answer(
            "❌ An error occurred while processing your voice message."
        )
