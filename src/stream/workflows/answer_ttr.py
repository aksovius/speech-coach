import os

from bytewax import operators as op
from bytewax.connectors.kafka import operators as kop
from bytewax.dataflow import Dataflow

from shared.logging import get_log_level, setup_logger
from stream.config import CLEAN_WORDS_TOPIC, KAFKA_BROKER
from stream.metrics import start_metrics_server
from stream.metrics_operators import map_with_metrics
from stream.processors.deserialize import parse_kafka_message
from stream.processors.text_processor import calculate_ttr_simple
from stream.sinks.clickhouse import ClickHouseSink

start_metrics_server(port=9092)

# Configure logger with Loki formatter
logger = setup_logger(
    name="bytewax.answer_ttr",
    level=get_log_level(os.getenv("LOG_LEVEL", "INFO")),
    service=os.getenv("LOG_SERVICE", "speech-coach"),
    component="bytewax.answer_ttr",
    use_loki=True,
)

logger.info(
    "Starting answer TTR flow",
    extra={
        "event": "flow_start",
        "broker": KAFKA_BROKER,
        "input_topic": CLEAN_WORDS_TOPIC,
    },
)

flow = Dataflow("answer_ttr_flow")
inp = kop.input("in", flow, brokers=[KAFKA_BROKER], topics=[CLEAN_WORDS_TOPIC])
clickhouse_sink = ClickHouseSink(
    "answer_ttr", ["user_id", "timestamp", "ttr", "score_overall"]
)
oks = inp.oks

# 1. Deserialization → filtering
deserialized = map_with_metrics("deserialize", oks, parse_kafka_message)
logger.debug("Messages deserialized", extra={"event": "deserialize_complete"})

# 2. Calculate TTR
ttr = map_with_metrics("calculate_ttr", deserialized, calculate_ttr_simple)
logger.debug("TTR calculated", extra={"event": "ttr_calculated"})


def insert_batch_to_clickhouse(ttr):
    if not ttr:
        return
    logger.info(
        "Inserting batch to ClickHouse",
        extra={
            "event": "clickhouse_insert",
            "batch_size": len(ttr) if isinstance(ttr, list) else 1,
        },
    )


op.output("insert_batch_to_clickhouse", ttr, clickhouse_sink)
logger.info("Flow configured", extra={"event": "flow_configured"})
