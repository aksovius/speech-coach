import os

from shared.logging import get_log_level, setup_logger
from shared.messaging.broker import broker
from shared.schemas.audio_schema import AudioTaskProcessing, AudioTaskResult
from shared.services import audio_processing, upload_service
from worker.metrics.worker import (
    PROCESSED_MESSAGES,
    PROCESSING_ERRORS,
    PROCESSING_LATENCY,
)

# Configure logger with Loki formatter
logger = setup_logger(
    name="worker.audio_consumer",
    level=get_log_level(os.getenv("LOG_LEVEL", "INFO")),
    service=os.getenv("LOG_SERVICE", "speech-coach"),
    component="worker.audio_consumer",
    use_loki=True,
)


@broker.subscriber(stream="audio_stream")
async def handle_task(data: AudioTaskProcessing):
    """Handle audio processing task."""
    logger.info(
        "Message received",
        extra={
            "event": "task_received",
            "telegram_id": data.telegram_id,
            "user_id": data.user_id,
            "file_path": data.file_path,
            "question_category": data.question_category,
        },
    )

    task_output = AudioTaskResult(
        telegram_id=data.telegram_id,
        user_id=data.user_id,
        converted_file="",
        uploaded_file="",
        question_category=data.question_category,
    )

    try:
        # Process audio file
        logger.info(
            "Starting audio processing",
            extra={
                "event": "processing_start",
                "file_path": data.file_path,
                "question_category": data.question_category,
            },
        )

        time_limit = 45
        stream = ""
        match data.question_category:
            case "toefl1":
                time_limit = 45
                stream = "toefl_response_stream"
            case "toefl2":
                time_limit = 60
                stream = "toefl_response_stream"
            case "general" | "architecture" | "frontend" | "backend" | "interview":
                time_limit = 180
                stream = "question_response_stream"
        # Measure processing time and track metrics
        with PROCESSING_LATENCY.labels(message_type="audio").time():
            converted_file = await audio_processing.process_audio(
                data.file_path, time_limit=time_limit, speed_factor=1.0
            )
            if not converted_file:
                raise ValueError("Failed to process the audio file.")

        logger.info(
            "Audio processing completed",
            extra={
                "event": "processing_complete",
                "converted_file": converted_file,
                "question_category": data.question_category,
            },
        )

        # Upload file
        logger.info(
            "Starting file upload",
            extra={
                "event": "upload_start",
                "file_path": data.file_path,
                "question_category": data.question_category,
            },
        )
        uploaded_file = await upload_service.upload_file(data.file_path)

        logger.info(
            "File upload completed",
            extra={
                "event": "upload_complete",
                "uploaded_file": uploaded_file,
                "question_category": data.question_category,
            },
        )

        task_output.converted_file = converted_file
        task_output.uploaded_file = uploaded_file
        logger.info(
            "Task completed successfully",
            extra={
                "event": "task_success",
                "converted_file": converted_file,
                "uploaded_file": uploaded_file,
                "question_category": data.question_category,
            },
        )

        # Increment success counter
        PROCESSED_MESSAGES.labels(message_type="audio").inc()

    except Exception as e:
        logger.error(
            "Error processing task",
            extra={
                "event": "task_error",
                "file_path": data.file_path,
                "error": str(e),
                "question_category": data.question_category,
            },
        )
        task_output.error = str(e)

        # Track error
        PROCESSING_ERRORS.labels(
            message_type="audio", error_type=type(e).__name__
        ).inc()

    finally:
        # Cleanup
        try:
            if os.path.exists(data.file_path):
                os.remove(data.file_path)
                logger.info(
                    "Removed temporary file",
                    extra={
                        "event": "file_cleanup",
                        "file_path": data.file_path,
                        "question_category": data.question_category,
                    },
                )
        except Exception as e:
            logger.error(
                "Failed to remove temporary file",
                extra={
                    "event": "cleanup_error",
                    "file_path": data.file_path,
                    "error": str(e),
                    "question_category": data.question_category,
                },
            )

        # Publish response
        try:
            await broker.publish(task_output, stream=stream)
            logger.info(
                "Published response",
                extra={
                    "event": "response_published. stream: " + stream,
                    "telegram_id": task_output.telegram_id,
                    "user_id": task_output.user_id,
                    "has_error": bool(task_output.error),
                    "question_category": data.question_category,
                },
            )
        except Exception as e:
            logger.error(
                "Failed to publish response",
                extra={
                    "event": "publish_error",
                    "error": str(e),
                    "question_category": data.question_category,
                },
            )
