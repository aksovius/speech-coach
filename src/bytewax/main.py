from bytewax import operators as op
from bytewax.connectors.kafka import operators as kop
from bytewax.connectors.stdio import StdOutSink
from bytewax.dataflow import Dataflow

flow = Dataflow("test")
inp = kop.input("in", flow, brokers=["redpanda:9092"], topics=["postgres_.public.user_answers"])
op.output("out", inp.oks, StdOutSink())