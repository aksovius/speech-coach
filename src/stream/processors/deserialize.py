import json
import os

from shared.logging import get_log_level, setup_logger

# from schemas.answer_schema import Answer

# Configure logger with Loki formatter
logger = setup_logger(
    name="bytewax.deserialize",
    level=get_log_level(os.getenv("LOG_LEVEL", "INFO")),
    service=os.getenv("LOG_SERVICE", "speech-coach"),
    component="bytewax.deserialize",
    use_loki=True,
)


def deserialize_message(kafka_message):
    try:
        if not kafka_message.value:
            logger.debug("Empty message value", extra={"event": "deserialize_skip"})
            return None

        value = json.loads(kafka_message.value.decode())
        payload = value.get("payload")

        if payload is None:
            logger.debug("No payload in message", extra={"event": "deserialize_skip"})
            return None

        # Process both snapshot (r) and insert/update
        if payload.get("op") not in ("c", "u", "r"):
            logger.debug(
                "Unsupported operation",
                extra={
                    "event": "deserialize_skip",
                    "operation": payload.get("op"),
                },
            )
            return None

        after = payload.get("after")
        if after is None:
            logger.debug("No after data", extra={"event": "deserialize_skip"})
            return None

        #   answer = Answer(**after)
        # logger.info(f"Validated: {answer}")

        # return {
        #     "id": answer.id,
        #     "user_id": answer.user_id,
        #     "asr_transcript": answer.asr_transcript,
        #     "operation": payload.get("op"),
        #     "ts_ms": payload.get("ts_ms"),
        # }
        result = {
            "id": after.get("id"),
            "user_id": after.get("user_id"),
            "asr_transcript": after.get("asr_transcript"),
            "created_at": after.get("created_at"),
            "score_overall": after.get("score_overall"),
            "operation": payload.get("op"),
            "ts_ms": payload.get("ts_ms"),
        }

        logger.debug(
            "Message deserialized",
            extra={
                "event": "deserialize_success",
                "message_id": result["id"],
                "user_id": result["user_id"],
            },
        )
        return result

    except Exception as e:
        logger.error(
            "Deserialization error",
            extra={
                "event": "deserialize_error",
                "error": str(e),
            },
        )
        return None


def parse_kafka_message(msg):
    try:
        key = msg.key.decode() if msg.key else None
        val = json.loads(msg.value.decode())
        result = {"key": key, **val}

        logger.debug(
            "Message parsed",
            extra={
                "event": "parse_success",
                "key": key,
            },
        )
        return result
    except Exception as e:
        logger.error(
            "Message parsing error",
            extra={
                "event": "parse_error",
                "error": str(e),
            },
        )
        return None
