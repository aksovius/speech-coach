from functools import partial

from bytewax import operators as op
from bytewax.connectors.kafka import operators as kop
from bytewax.dataflow import Dataflow
from processors.aggregators import sliding_avg_builder, unique_words_builder
from processors.deserialize import parse_kafka_message
from processors.formaters import format_avg
from processors.text_processing import extract_words

from config import CLEAN_WORDS_TOPIC, KAFKA_BROKER

flow = Dataflow("average_five_flow")
inp = kop.input("in", flow, brokers=[KAFKA_BROKER], topics=[CLEAN_WORDS_TOPIC])

oks = inp.oks

# 1. Deserialization → filtering
deserialized = op.map("deserialize", oks, parse_kafka_message)
# op.inspect("inspect_words", deserialized)
words = op.map("extract_words", deserialized, extract_words)
# op.inspect("inspect_words", words)
# # Group by user_id
keyed = op.key_on("key_by_user", words, lambda x: str(x[0]["user_id"]))

# # Count unique words
unique_counts = op.stateful_map("count_unique_words", keyed, unique_words_builder())

N = 5
sliding_avg = op.stateful_map(
    "sliding_avg_last_5", unique_counts, sliding_avg_builder(N)
)

sliding_avg_last_5 = op.map("format_avg_avg", sliding_avg, partial(format_avg, N=5))
op.inspect("inspect_avg", sliding_avg_last_5)
# kafka_messages = op.map("to_kafka_msg", sliding_avg_last_5, to_kafka_message)

# op.output("out_avg", sliding_avg_last_5, StdOutSink())
# kop.output(
#     "kafka-output",
#     kafka_messages,
#     brokers=['192.168.1.86:19092'],
#     topic="clean_words"
# )
