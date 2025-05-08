import logging
import time
from contextlib import asynccontextmanager
from datetime import UTC, datetime

from aiogram.types import Update
from fastapi import FastAPI, Request
from fastapi.logger import logger as fastapi_logger
from fastapi.middleware.cors import CORSMiddleware
from faststream import FastStream
from prometheus_client import make_asgi_app
from prometheus_fastapi_instrumentator import Instrumentator

import server.consumers.architecture_consumer  # noqa: F401   !DO NOT REMOVE
import server.consumers.audio_consumer  # noqa: F401   !DO NOT REMOVE
from server.api.routes import statistics
from server.bot.dp import bot, dp, set_commands
from shared.config import settings
from shared.logging import get_log_level, setup_logger
from shared.messaging.broker import broker

from .metrics import (
    TELEGRAM_MESSAGE_TYPES,
    TELEGRAM_REQUEST_LATENCY,
    TELEGRAM_REQUESTS,
)
from .middlewares.metrics import metrics_middleware

# Configure logger with Loki formatter
logger = setup_logger(
    name="server",
    level=get_log_level(settings.LOG_LEVEL),
    service=settings.LOG_SERVICE,
    component="server",
    use_loki=True,
)

# Disable logging for GET /metrics requests and set up root logger
logging.getLogger().setLevel(logging.WARNING)
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("fastapi").setLevel(logging.WARNING)


# Configure filter for uvicorn logs
class MetricsFilter(logging.Filter):
    def filter(self, record):
        return not (record.getMessage().find("GET /metrics") >= 0)


# Apply filter to uvicorn logger
uvicorn_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.addFilter(MetricsFilter())
fastapi_logger.addFilter(MetricsFilter())

WEBHOOK_PATH = f"/webhook/{settings.TELEGRAM_BOT_TOKEN}"
WEBHOOK_URL = f"https://{settings.APP_HOST}{WEBHOOK_PATH}"
faststream_app = FastStream(
    broker
)  # Create a FastStream app with the broker (receiver app)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    logger.info("Starting application", extra={"event": "startup"})
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    await set_commands()
    await broker.connect()  # start broker connection
    await faststream_app.start()
    logger.info(
        "Application started successfully",
        extra={"event": "startup_complete", "webhook_url": WEBHOOK_URL},
    )

    yield

    # SHUTDOWN
    logger.info("Shutting down application", extra={"event": "shutdown"})
    await bot.delete_webhook()
    await broker.close()
    await faststream_app.stop()
    logger.info("Application shutdown complete", extra={"event": "shutdown_complete"})


app = FastAPI(title="Speech Coach API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(statistics.router)

# Instrumentation
Instrumentator().instrument(app).expose(app)

# Mount Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Add metrics middleware
app.middleware("http")(metrics_middleware)


@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    start_time = time.time()
    data = await request.json()
    update = Update.model_validate(data)

    # Log incoming message
    logger.info(
        "Received Telegram webhook",
        extra={
            "event": "telegram_webhook",
            "update_type": (
                "message"
                if update.message
                else "callback_query" if update.callback_query else "unknown"
            ),
            "message_type": update.message.content_type if update.message else None,
        },
    )

    # Increment request counter
    update_type = (
        "message"
        if update.message
        else "callback_query" if update.callback_query else "unknown"
    )
    TELEGRAM_REQUESTS.labels(update_type=update_type).inc()

    # Process the update
    await dp.feed_update(bot, update)

    # Record latency
    latency = time.time() - start_time
    TELEGRAM_REQUEST_LATENCY.labels(update_type=update_type).observe(latency)

    # Count message types
    if update.message:
        TELEGRAM_MESSAGE_TYPES.labels(message_type=update.message.content_type).inc()

    logger.info(
        "Processed Telegram webhook",
        extra={
            "event": "telegram_webhook_processed",
            "latency": latency,
            "update_type": update_type,
        },
    )

    return {"ok": True}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now(UTC).isoformat(),
    }
