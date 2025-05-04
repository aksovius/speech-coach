import os

from bytewax.connectors.kafka import operators as kop
from bytewax.dataflow import Dataflow

from shared.logging import get_log_level, setup_logger
from stream.config import CLEAN_WORDS_TOPIC, DEBEZIUM_TOPIC, KAFKA_BROKER
from stream.metrics import start_metrics_server
from stream.metrics_operators import filter_with_metrics, map_with_metrics
from stream.processors.deserialize import deserialize_message
from stream.processors.filters import filter_empty_transcript, filter_none
from stream.processors.formaters import to_kafka_message
from stream.processors.text_processor import normalize_text

# Запускаем сервер метрик
start_metrics_server(port=9091)

# Configure logger with Loki formatter
logger = setup_logger(
    name="bytewax.cleanup",
    level=get_log_level(os.getenv("LOG_LEVEL", "INFO")),
    service=os.getenv("LOG_SERVICE", "speech-coach"),
    component="bytewax.cleanup",
    use_loki=True,
)

logger.info(
    "Starting cleanup flow",
    extra={
        "event": "flow_start",
        "broker": KAFKA_BROKER,
        "input_topic": DEBEZIUM_TOPIC,
        "output_topic": CLEAN_WORDS_TOPIC,
    },
)

flow = Dataflow("cleanup_flow")
inp = kop.input("in", flow, brokers=[KAFKA_BROKER], topics=[DEBEZIUM_TOPIC])

oks = inp.oks

# 1. Deserialization → filtering
deserialized = map_with_metrics("deserialize", oks, deserialize_message)
logger.debug("Messages deserialized", extra={"event": "deserialize_complete"})

# 2. Filter empty and None values
clean = filter_with_metrics("not_none", deserialized, filter_none)
clean = filter_with_metrics("has_text", clean, filter_empty_transcript)
logger.debug("Messages filtered", extra={"event": "filter_complete"})

# 3. Normalize text
normed = map_with_metrics("normalize", clean, normalize_text)
logger.debug("Text normalized", extra={"event": "normalize_complete"})

# 4. Format and send to Kafka
kafka_messages = map_with_metrics("to_kafka_msg", normed, to_kafka_message)
kop.output(
    "kafka-output", kafka_messages, brokers=[KAFKA_BROKER], topic=CLEAN_WORDS_TOPIC
)
logger.info("Flow configured", extra={"event": "flow_configured"})
