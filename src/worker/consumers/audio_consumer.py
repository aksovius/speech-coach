import logging
import os

from shared.messaging.broker import broker
from shared.schemas.audio_schema import AudioTaskProcessing, AudioTaskResult
from shared.services import audio_processing, upload_service

logging.basicConfig(
    filename="consumer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@broker.subscriber(stream="audio_stream")
async def handle_task(data: AudioTaskProcessing):
    """Handle audio processing task."""
    logger.info("🔥 MESSAGE RECEIVED: %s", data)
    print("🔥 MESSAGE RECEIVED:", data)

    task_output = AudioTaskResult(
        telegram_id=data.telegram_id,
        user_id=data.user_id,
        converted_file="",
        uploaded_file="",
    )

    try:
        # Process audio file
        logger.info("Starting audio processing for file: %s", data.file_path)
        converted_file = await audio_processing.process_audio(
            data.file_path, time_limit=45, speed_factor=1.0
        )
        if not converted_file:
            raise ValueError("Failed to process the audio file.")
        logger.info("Audio processing completed: %s", converted_file)

        # Upload file
        logger.info("Starting file upload: %s", data.file_path)
        uploaded_file = await upload_service.upload_file(data.file_path)
        logger.info("File upload completed: %s", uploaded_file)

        task_output.converted_file = converted_file
        task_output.uploaded_file = uploaded_file
        logger.info("Task completed successfully for file: %s", data.file_path)

    except Exception as e:
        logger.error("Error processing task for file %s: %s", data.file_path, str(e))
        task_output.error = str(e)

    finally:
        # Cleanup
        try:
            if os.path.exists(data.file_path):
                os.remove(data.file_path)
                logger.info("Removed temporary file: %s", data.file_path)
        except Exception as e:
            logger.error(
                "Failed to remove temporary file %s: %s", data.file_path, str(e)
            )

        # Publish response
        try:
            await broker.publish(task_output, stream="audio_response_stream")
            logger.info("Published response: %s", task_output)
        except Exception as e:
            logger.error("Failed to publish response: %s", str(e))
