from bytewax import operators as op
from bytewax.connectors.kafka import operators as kop
from bytewax.connectors.stdio import StdOutSink
from bytewax.dataflow import Dataflow

from config import KAFKA_BROKER, TOPIC

print("Starting Kafka consumer...")
print(KAFKA_BROKER)
print(TOPIC)
flow = Dataflow("speech_flow")
inp = kop.input("in", flow, brokers=[KAFKA_BROKER], topics=[TOPIC])
op.output("out", inp.oks, StdOutSink())
