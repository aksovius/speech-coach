import os

from bytewax import operators as op
from bytewax.connectors.kafka import operators as kop
from bytewax.connectors.stdio import StdOutSink
from bytewax.dataflow import Dataflow
from config import KAFKA_BROKER, TOPIC
from shared.logging import get_log_level, setup_logger

# Configure logger with Loki formatter
logger = setup_logger(
    name="bytewax",
    level=get_log_level(os.getenv("LOG_LEVEL", "INFO")),
    service=os.getenv("LOG_SERVICE", "speech-coach"),
    component="bytewax",
    use_loki=True,
)

logger.info(
    "Initializing Kafka consumer",
    extra={
        "event": "kafka_init",
        "broker": KAFKA_BROKER,
        "topic": TOPIC,
    },
)

flow = Dataflow("speech_flow")
inp = kop.input("in", flow, brokers=[KAFKA_BROKER], topics=[TOPIC])


def process_message(message):
    try:
        logger.info(
            "Processing message",
            extra={
                "event": "process_message",
                "message": message,
            },
        )
        return message
    except Exception as e:
        logger.error(
            "Error processing message",
            extra={
                "event": "process_message_error",
                "error": str(e),
            },
        )
        raise


# Add processing step
processed = op.map("process", inp.oks, process_message)

# Output to stdout for debugging
op.output("out", processed, StdOutSink())


def main():
    logger.info("Starting bytewax processor", extra={"event": "startup"})
    flow.run()
    logger.info("Bytewax processor completed", extra={"event": "shutdown"})


if __name__ == "__main__":
    main()
