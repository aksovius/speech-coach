import json

def deserialize_message(kafka_message):
    try:
        if not kafka_message.value:
            return None
        value = json.loads(kafka_message.value.decode())
        payload = value.get("payload")
        if payload is None or payload.get("op") not in ("c", "u"):
            return None
        after = payload.get("after") or {}
        return {
            "id":          after.get("id"),
            "user_id":     after.get("user_id"),
            "asr_transcript": after.get("asr_transcript"),
            "operation":   payload.get("op"),
            "ts_ms":       payload.get("ts_ms"),
        }
    except Exception as e:
        # логируем, чтобы не ломать поток
        print(f"deserialize error: {e}")
        return None
