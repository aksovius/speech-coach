import asyncio

from faststream import FastStream
from prometheus_client import start_http_server

import worker.consumers.audio_consumer  # noqa: F401   !DO NOT REMOVE
from shared.config import settings
from shared.logging import get_log_level, setup_logger
from shared.messaging.broker import broker

# Configure logger with Loki formatter
logger = setup_logger(
    name="worker",
    level=get_log_level(settings.LOG_LEVEL),
    service=settings.LOG_SERVICE,
    component="worker",
    use_loki=True,
)

# Create FastStream app
app = FastStream(broker)


def main():
    """Main entry point for the worker."""
    logger.info("Starting worker", extra={"event": "startup"})

    # Start Prometheus metrics server
    start_http_server(8001)
    logger.info(
        "Metrics server started on port 8001", extra={"event": "metrics_startup"}
    )

    # Run FastStream app
    asyncio.run(app.run())


if __name__ == "__main__":
    main()
