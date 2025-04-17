from bytewax.dataflow import Dataflow
from bytewax import operators as op
from bytewax.connectors.kafka import operators as kop

import processors.deserialize    as des
import processors.filters        as flt
import processors.text_processing as txt
import processors.aggregators    as agg
import sinks                      as sk

flow = Dataflow("speech_flow")

inp = kop.input("in", flow,
    brokers=["redpanda:9092"],
    topics=["postgres_.public.user_answers"],
)

# 1. Десериализация → фильтрация
deser = op.map("deserialize", inp.oks, des.deserialize_message)
clean = op.filter("not_none", deser, flt.filter_none)
clean = op.filter("has_text", clean, flt.filter_empty_transcript)

# 2. Текстовые трансформации
normed = op.map("normalize", clean, txt.normalize_text)
words  = op.map("extract_words", normed, txt.extract_words)

# 3. KeyedStream + агрегаты
keyed = op.key_on("by_user", words, lambda x: str(x[0]["user_id"]))

unique = op.stateful_map("unique", keyed, agg.unique_words_builder())
avg5   = op.stateful_map("avg5",   unique, agg.sliding_avg_builder(5))

# 4. Форматирование и output
fmt_unique = op.map("fmt_unique", unique,
    lambda kv: {"user_id": kv[0], "unique": kv[1]}
)
fmt_avg5 = op.map("fmt_avg5", avg5,
    lambda kv: {"user_id": kv[0], "avg_last_5": kv[1]}
)

sk.stdout_sink(flow, "fmt_unique")
sk.kafka_sink (flow, "fmt_avg5", topic="avg_unique_counts")
