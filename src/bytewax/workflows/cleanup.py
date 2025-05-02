from processors.deserialize import deserialize_message
from processors.filters import filter_empty_transcript, filter_none
from processors.formaters import to_kafka_message
from processors.text_processor import normalize_text

from bytewax import operators as op
from bytewax.connectors.kafka import operators as kop
from bytewax.dataflow import Dataflow
from config import CLEAN_WORDS_TOPIC, DEBEZIUM_TOPIC, KAFKA_BROKER

print("Starting cleanup flow...")
flow = Dataflow("cleanup_flow")
inp = kop.input("in", flow, brokers=[KAFKA_BROKER], topics=[DEBEZIUM_TOPIC])

oks = inp.oks
# 1. Deserialization → filtering
deserialized = op.map("deserialize", oks, deserialize_message)
clean = op.filter("not_none", deserialized, filter_none)
clean = op.filter("has_text", clean, filter_empty_transcript)

normed = op.map("normalize", clean, normalize_text)

kafka_messages = op.map("to_kafka_msg", normed, to_kafka_message)
kop.output(
    "kafka-output", kafka_messages, brokers=[KAFKA_BROKER], topic=CLEAN_WORDS_TOPIC
)
