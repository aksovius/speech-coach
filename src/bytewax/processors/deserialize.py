import json

# from schemas.answer_schema import Answer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def deserialize_message(kafka_message):
    try:
        if not kafka_message.value:
            return None

        value = json.loads(kafka_message.value.decode())
        payload = value.get("payload")

        if payload is None:
            return None

        # Обрабатываем и snapshot (r), и insert/update
        if payload.get("op") not in ("c", "u", "r"):
            return None

        after = payload.get("after")
        if after is None:
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
        return {
            "id": after.get("id"),
            "user_id": after.get("user_id"),
            "asr_transcript": after.get("asr_transcript"),
            "created_at": after.get("created_at"),
            "score_overall": after.get("score_overall"),
            "operation": payload.get("op"),
            "ts_ms": payload.get("ts_ms"),
        }

    except Exception:
        logger.exception("Deserialization error")
        return None


def parse_kafka_message(msg):
    key = msg.key.decode() if msg.key else None
    val = json.loads(msg.value.decode())
    return {"key": key, **val}
