import os
from datetime import datetime, timedelta, timezone

from bytewax import operators as op
from bytewax.connectors.kafka import operators as kop
from bytewax.dataflow import Dataflow
from bytewax.operators.windowing import (
    EventClock,
    TumblingWindower,
    reduce_window,
)

from shared.logging import get_log_level, setup_logger
from stream.config import CLEAN_WORDS_TOPIC, KAFKA_BROKER
from stream.metrics import start_metrics_server
from stream.metrics_operators import map_with_metrics
from stream.processors.deserialize import parse_kafka_message
from stream.processors.text_processor import lemmatize_text
from stream.sinks.clickhouse import ClickHouseSink

start_metrics_server(port=9093)
now_aligned = datetime(2025, 5, 1, tzinfo=timezone.utc)
# Configure logger with Loki formatter
logger = setup_logger(
    name="bytewax.active_words",
    level=get_log_level(os.getenv("LOG_LEVEL", "INFO")),
    service=os.getenv("LOG_SERVICE", "speech-coach"),
    component="bytewax.active_words",
    use_loki=True,
)

logger.info(
    "Starting active words flow",
    extra={
        "event": "flow_start",
        "broker": KAFKA_BROKER,
        "input_topic": CLEAN_WORDS_TOPIC,
    },
)

flow = Dataflow("active_words_flow")
inp = kop.input("in", flow, brokers=[KAFKA_BROKER], topics=[CLEAN_WORDS_TOPIC])
clickhouse_sink = ClickHouseSink(
    "active_words", ["user_id", "timestamp", "word", "word_count"]
)
oks = inp.oks

# 1. Deserialization → filtering
deserialized = map_with_metrics("deserialize", oks, parse_kafka_message)
logger.debug("Messages deserialized", extra={"event": "deserialize_complete"})

# 2. Calculate unique words
lemmatized_stream = op.flat_map("normalize", deserialized, lemmatize_text)
print("type(lemmatized_stream)", type(lemmatized_stream))
# op.inspect("lemmatized_stream", lemmatized_stream)

window = TumblingWindower(timedelta(days=1), now_aligned)

keyed = lemmatized_stream.then(
    op.key_on, "by_user_word", lambda x: f"{x['user_id']}:{x['word']}"
)


def extract_event_time(msg):
    return msg["timestamp"]


def init():
    return {"count": 0, "timestamp": None}


def add(acc, item):
    acc["count"] += int(item.get("count", 1))
    acc["timestamp"] = item.get("timestamp")
    return acc


def finalize(acc):
    return acc


clock = EventClock(extract_event_time, wait_for_system_duration=timedelta(seconds=0))

aggregated = reduce_window(
    "30d_word_count", keyed, clock=clock, windower=window, reducer=add
)

aggregated_down = aggregated.down

op.inspect("aggregated", aggregated_down)


def format_for_clickhouse(row):
    key, (window_meta, data) = row
    user_id, word = key.split(":")
    return {
        "user_id": int(user_id),
        "timestamp": data["timestamp"],
        "word": word,
        "word_count": data["count"],
    }


formatted = op.map("prepare_for_clickhouse", aggregated_down, format_for_clickhouse)
op.inspect("formatted", formatted)
op.output("clickhouse_output", formatted, clickhouse_sink)

# op.output("insert_batch_to_clickhouse", ttr, clickhouse_sink)
logger.info("Flow configured", extra={"event": "flow_configured"})
