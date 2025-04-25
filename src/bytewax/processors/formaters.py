import json

from bytewax.connectors.kafka import KafkaSinkMessage


def format_avg(key__data, N):
    user_id, avg = key__data
    return {"user_id": user_id, f"avg_unique_words_last_{N}": avg}


def to_kafka_message(item) -> KafkaSinkMessage:
    key = str(item.get("user_id", "none")).encode("utf-8")
    val = json.dumps(item).encode("utf-8")
    return KafkaSinkMessage(key=key, value=val)
