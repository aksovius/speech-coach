import json

from bytewax.connectors.kafka import KafkaSinkMessage


def to_kafka_message(item) -> KafkaSinkMessage:
    key = str(item.get("user_id", "none")).encode("utf-8")
    val = json.dumps(item).encode("utf-8")
    return KafkaSinkMessage(key=key, value=val)
