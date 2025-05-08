import os
import uuid
from typing import Dict

from shared.logging import get_log_level, setup_logger
from shared.messaging.broker import broker
from shared.schemas.audio_schema import AudioTaskProcessing
from shared.services import download_service

logger = setup_logger(
    name="worker.audio_service",
    level=get_log_level(os.getenv("LOG_LEVEL", "INFO")),
    service=os.getenv("LOG_SERVICE", "speech-coach"),
    component="worker.audio_service",
    use_loki=True,
)


async def process_voice_message(
    file_url: str, user_id: int, telegram_id: int, question_category: str = "general"
) -> Dict[str, str]:
    ogg_path = f"shared/temp/{uuid.uuid4()}.ogg"
    # Download the audio file
    downloaded_file = await download_service.download_file(file_url, ogg_path)
    if not downloaded_file:
        return {"error": "Failed to download the audio file."}
    message = AudioTaskProcessing(
        telegram_id=telegram_id,
        user_id=user_id,
        file_path=downloaded_file,
        question_category=question_category,
    )
    logger.info(
        "Processing voice message",
        extra={
            "event": "processing_start",
            "file_path": downloaded_file,
            "question_category": question_category,
        },
    )
    await broker.publish(
        message,
        stream="audio_stream",
    )
    # # Convert OGG to WAV
    # converted_file = await audio_processing.convert_ogg_to_mp3(downloaded_file)
    # if not converted_file:
    #     return {"error": "Failed to convert the audio file."}

    # transcription = await transcribe_audio(converted_file)
    # file = await upload_service.upload_file(downloaded_file)
    # print(f"File uploaded to: {file}")
    # if not transcription:
    #     return {"error": "Failed to transcribe the audio file."}
    # answer = await evaluate_answer(question.text, transcription)
    # user_answer = UserAnswer(
    #     user_id=user_id,
    #     question_id=question.id,
    #     asr_transcript=transcription,
    #     gpt_feedback=answer,
    #     score_overall=0,
    # )
    # await answers_service.save_answer(user_answer, db)
    # print(f"Transcription: {transcription}")
    # print(f"Answer: {answer}")
    # if not answer:
    #     return {"error": "Failed to evaluate the answer."}
    # return {"transcription": transcription, "answer": answer}
