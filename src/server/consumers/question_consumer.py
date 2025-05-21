import os

from server.ai.services.audio_service import transcribe_audio
from server.ai.services.question_service import evaluate_question
from server.bot.dp import bot
from server.bot.keyboards.menu_keyboards import (
    MODE_ARCHITECTURE_START,
    get_next_back_keyboard,
)
from server.models.schema import Media, UserAnswer
from server.utils.database import async_session
from shared.messaging.broker import broker
from shared.schemas.audio_schema import AudioTaskResult
from shared.services import answers_service, media_service
from shared.services.question_manager import get_user_question


@broker.subscriber(stream="question_response_stream")
async def handle_question_task(result: AudioTaskResult):
    telegram_id = result.telegram_id
    question_category = result.question_category

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
    print(f"Transcription: {transcription}")

    if not transcription:
        await bot.send_message(
            chat_id=telegram_id,
            text="<b>❌ Error:</b> Failed to transcribe the audio file.",
            parse_mode="HTML",
        )
        return

    evaluation = await evaluate_question(
        question.text, transcription, question_category
    )
    print(f"Evaluation: {evaluation}")

    if isinstance(evaluation, str):
        await bot.send_message(
            chat_id=telegram_id,
            text=f"<b>❌ Error:</b> {evaluation}",
            parse_mode="HTML",
        )
        return

    user_answer = UserAnswer(
        user_id=user_id,
        question_id=question.id,
        asr_transcript=transcription,
        gpt_feedback=(
            ", ".join(evaluation.feedback)
            if evaluation.feedback
            else "No feedback provided"
        ),
        score_overall=evaluation.total_score,
    )

    media = Media(
        source_type="user_answer",
        media_type="audio",
        url=converted_file,
        description=transcription or "Transcription not available",
    )

    # Send results to user
    if transcription:
        await bot.send_message(
            chat_id=telegram_id,
            text=f"<b>User:</b> {transcription}",
            parse_mode="HTML",
        )

    # Send evaluation scores
    await bot.send_message(
        chat_id=telegram_id,
        text=(
            f"<b>📊 Evaluation:</b>\n"
            f"• Content: {evaluation.content_score}/50\n"
            f"• Language: {evaluation.language_score}/50\n"
            f"• Total Score: {evaluation.total_score}/100"
        ),
        parse_mode="HTML",
    )

    # Send strengths
    if evaluation.strengths:
        strengths_text = "\n".join([f"• {s}" for s in evaluation.strengths])
        await bot.send_message(
            chat_id=telegram_id,
            text=f"<b>💪 Strengths:</b>\n{strengths_text}",
            parse_mode="HTML",
        )

    # Send weaknesses
    if evaluation.weaknesses:
        weaknesses_text = "\n".join([f"• {w}" for w in evaluation.weaknesses])
        await bot.send_message(
            chat_id=telegram_id,
            text=f"<b>⚠️ Weaknesses:</b>\n{weaknesses_text}",
            parse_mode="HTML",
        )

    # Send suggestions
    if evaluation.suggestions:
        suggestions_text = "\n".join([f"• {s}" for s in evaluation.suggestions])
        await bot.send_message(
            chat_id=telegram_id,
            text=f"<b>💡 Suggestions:</b>\n{suggestions_text}",
            parse_mode="HTML",
        )

    # Send recommended answer
    await bot.send_message(
        chat_id=telegram_id,
        text=f"<b>📝 Recommended Answer:</b>\n{evaluation.recommended_answer}",
        parse_mode="HTML",
    )
    await bot.send_message(
        chat_id=telegram_id,
        text="Choose next action:",
        reply_markup=get_next_back_keyboard(MODE_ARCHITECTURE_START),
    )

    # Save results
    os.remove(converted_file)
    async with async_session() as session:
        answer_id = await answers_service.save_answer(user_answer, session)
        media.source_id = answer_id
        await media_service.save_media(media, session)
        print(f"Transcription: {transcription}")
        print(f"Evaluation: {evaluation}")


# Для обратной совместимости
@broker.subscriber(stream="architecture_response_stream")
async def handle_architecture_task(result: AudioTaskResult):
    # Добавляем тип вопроса, если его нет
    if not hasattr(result, "question_type"):
        result.question_type = "architecture"
    return await handle_question_task(result)
