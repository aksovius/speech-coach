import os

from server.ai.client import client
from shared.logging import get_log_level, setup_logger

# Configure logger with Loki formatter
logger = setup_logger(
    name="server.ai.audio",
    level=get_log_level(os.getenv("LOG_LEVEL", "INFO")),
    service=os.getenv("LOG_SERVICE", "speech-coach"),
    component="server.ai.audio",
    use_loki=True,
)


async def transcribe_audio(audio_path) -> str | None:
    logger.debug(
        "Transcription client initialized", extra={"client": str(type(client))}
    )
    logger.info(
        "Starting audio transcription",
        extra={"file_path": audio_path, "event": "transcription_start"},
    )
    try:
        with open(audio_path, "rb") as audio_file:
            response = await client.audio.transcriptions.create(  # type: ignore
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                # timestamp_granularities=["word"],
                language="en",
                temperature=0.0,
                prompt=None,
            )

        logger.info(
            "Transcription completed successfully",
            extra={"file_path": audio_path, "event": "transcription_success"},
        )
        return response.text
    except Exception as e:
        logger.error(
            "Failed to transcribe audio file",
            extra={
                "error": str(e),
                "file_path": audio_path,
                "event": "transcription_error",
            },
        )
        return None
