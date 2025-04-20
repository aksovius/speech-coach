import logging
import os

from messaging.broker import broker
from schemas.audio_schema import AudioTaskProcessing, AudioTaskResult
from services import audio_processing, upload_service

logging.basicConfig(
    filename="consumer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@broker.subscriber(stream="audio_stream")
async def handle_task(data: AudioTaskProcessing):
    print("🔥 ПРИШЛО СООБЩЕНИЕ:", data)

    task_output = AudioTaskResult(
        telegram_id=data.telegram_id,
        user_id=data.user_id,
        converted_file="",
        uploaded_file="",
    )
    try:
        converted_file = await audio_processing.convert_ogg_to_wav(data.file_path)
        if not converted_file:
            raise ValueError("Failed to convert the audio file.")

        uploaded_file = await upload_service.upload_file(data.file_path)

        task_output.converted_file = converted_file
        task_output.uploaded_file = uploaded_file
        logger.info("Task completed successfully for file: %s", data.file_path)

    except Exception as e:
        logger.error("Error processing task for file %s: %s", data.file_path, str(e))
        task_output.error = str(e)

    finally:
        try:
            if os.path.exists(data.file_path):
                os.remove(data.file_path)
                logger.info("Removed temporary file: %s", data.file_path)
        except Exception as e:
            logger.error(
                "Failed to remove temporary file %s: %s", data.file_path, str(e)
            )

        await broker.publish(task_output, stream="audio_response_stream")
        logger.info("Published response: %s", task_output)
