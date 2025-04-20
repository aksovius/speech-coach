import os

from ai.services.audio_service import transcribe_audio
from ai.services.chat_service import evaluate_answer
from bot.dp import bot
from messaging.broker import broker
from models.schema import Media, UserAnswer
from schemas.audio_schema import AudioTaskResult
from services import answers_service, media_service
from services.question_manager import get_user_question
from utils.database import async_session


@broker.subscriber(stream="audio_response_stream")
async def handle_task(result: AudioTaskResult):

    print("Получена результат:", result)
    telegram_id = result.telegram_id
    if result.error:
        await bot.send_message(
            chat_id=telegram_id, text="❌ Error: Failed to process the audio file."
        )
        return

    converted_file = result.converted_file
    user_id = result.user_id
    question = get_user_question(telegram_id)
    transcription = await transcribe_audio(converted_file)
    answer = await evaluate_answer(question.text, transcription)
    user_answer = UserAnswer(
        user_id=user_id,
        question_id=question.id,
        asr_transcript=transcription,
        gpt_feedback=answer,
        score_overall=0,
    )
    media = Media(
        source_type="user_answers",
        media_type="audio",
        url=converted_file,
        description=transcription or "Transcription not available",
    )
    if not answer or not transcription:
        await bot.send_message(
            chat_id=telegram_id, text="❌ Error: Failed to evaluate the answer."
        )
        return

    if transcription:
        await bot.send_message(
            chat_id=telegram_id, text=f"User transcription: {transcription}"
        )
    if answer:
        await bot.send_message(chat_id=telegram_id, text=f"Coach answer: {answer}")

    os.remove(converted_file)
    # Save the answer to the database
    async with async_session() as session:
        answer_id = await answers_service.save_answer(user_answer, session)
        media.source_id = answer_id
        await media_service.save_media(media, session)
        print(f"Transcription: {transcription}")
        print(f"Answer: {answer}")
