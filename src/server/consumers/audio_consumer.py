import os

from server.ai.services.audio_service import transcribe_audio
from server.ai.services.chat_service import evaluate_answer
from server.bot.dp import bot
from server.models.schema import Media, UserAnswer
from server.utils.database import async_session
from shared.messaging.broker import broker
from shared.schemas.audio_schema import AudioTaskResult
from shared.services import answers_service, media_service
from shared.services.question_manager import get_user_question


@broker.subscriber(stream="audio_response_stream")
async def handle_task(result: AudioTaskResult):

    telegram_id = result.telegram_id
    if result.error:
        await bot.send_message(
            chat_id=telegram_id,
            text="<b>❌ Error:</b> Failed to process the audio file.",
            parse_mode="HTML",
        )
        return

    converted_file = result.converted_file
    user_id = result.user_id
    question = get_user_question(telegram_id)
    transcription = await transcribe_audio(converted_file)
    answer = await evaluate_answer(question.text, transcription)
    print(f"Answer: {answer}")
    user_answer = UserAnswer(
        user_id=user_id,
        question_id=question.id,
        asr_transcript=transcription,
        gpt_feedback=answer.feedback,
        score_overall=answer.score,
    )
    media = Media(
        source_type="user_answer",
        media_type="audio",
        url=converted_file,
        description=transcription or "Transcription not available",
    )
    if not answer or not transcription:
        await bot.send_message(
            chat_id=telegram_id,
            text="<b>❌ Error:</b> Failed to evaluate the answer.",
            parse_mode="HTML",
        )
        return

    if transcription:
        await bot.send_message(
            chat_id=telegram_id,
            text=f"<b>User:</b> {transcription}",
            parse_mode="HTML",
        )
    if answer:
        await bot.send_message(
            chat_id=telegram_id,
            text=f"<b>Coach:</b> {answer.feedback}",
            parse_mode="HTML",
        )
        await bot.send_message(
            chat_id=telegram_id, text=f"<b>Score:</b> {answer.score}", parse_mode="HTML"
        )
        await bot.send_message(
            chat_id=telegram_id,
            text=f"<b>Example:</b> {answer.example_answer}",
            parse_mode="HTML",
        )

    os.remove(converted_file)
    # Save the answer to the database
    async with async_session() as session:
        answer_id = await answers_service.save_answer(user_answer, session)
        media.source_id = answer_id
        await media_service.save_media(media, session)
        print(f"Transcription: {transcription}")
        print(f"Answer: {answer}")
