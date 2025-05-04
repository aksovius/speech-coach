import os

from bytewax import operators as op
from bytewax.connectors.kafka import operators as kop
from bytewax.dataflow import Dataflow

from shared.logging import get_log_level, setup_logger
from stream.config import CLEAN_WORDS_TOPIC, KAFKA_BROKER
from stream.processors.deserialize import parse_kafka_message
from stream.processors.text_processor import calculate_ttr_simple
from stream.sinks.clickhouse import ClickHouseSink

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
deserialized = op.map("deserialize", oks, parse_kafka_message)
logger.debug("Messages deserialized", extra={"event": "deserialize_complete"})

# 2. Calculate TTR
ttr = op.map("extract_words", deserialized, calculate_ttr_simple)
logger.debug("TTR calculated", extra={"event": "ttr_calculated"})

# op.inspect("inspect_words", ttr)
# # Group by user_id
# keyed = op.key_on("key_by_user", words, lambda x: str(x[0]["user_id"]))

# # Count unique words
# unique_counts = op.stateful_map("count_unique_words", keyed, unique_words_builder())

# N = 5
# sliding_avg = op.stateful_map(
#     "sliding_avg_last_5", unique_counts, sliding_avg_builder(N)
# )

# calculate_ttr = op.map("calculate_ttr", words, calculate_ttr_from_words)
# op.inspect("inspect_format_ttr", calculate_ttr)


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
    # clickhouse_client.insert(
    #     "speech.ttr_per_answer",
    #     [ttr],
    #     column_names=['user_id', 'timestamp', 'ttr']
    # )


op.output("insert_batch_to_clickhouse", ttr, clickhouse_sink)
logger.info("Flow configured", extra={"event": "flow_configured"})
