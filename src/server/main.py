import logging
import time
from contextlib import asynccontextmanager

from aiogram.types import Update
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from faststream import FastStream
from prometheus_client import Counter, Histogram
from prometheus_fastapi_instrumentator import Instrumentator

import server.consumers.audio_consumer  # noqa: F401   !DO NOT REMOVE
from server.bot.dp import bot, dp, set_commands
from shared.config import settings
from shared.messaging.broker import broker

logger = logging.getLogger(__name__)
WEBHOOK_PATH = f"/webhook/{settings.TELEGRAM_BOT_TOKEN}"
WEBHOOK_URL = f"https://{settings.APP_HOST}{WEBHOOK_PATH}"
faststream_app = FastStream(
    broker
)  # Create a FastStream app with the broker (receiver app)

# HTTP Metrics
REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "HTTP request latency", ["method", "endpoint"]
)

# Telegram Bot Metrics
TELEGRAM_REQUESTS = Counter(
    "telegram_requests_total",
    "Total number of Telegram bot requests",
    ["update_type"],  # message, callback_query, etc.
)

TELEGRAM_REQUEST_LATENCY = Histogram(
    "telegram_request_duration_seconds",
    "Time spent processing Telegram requests",
    ["update_type"],
)

TELEGRAM_MESSAGE_TYPES = Counter(
    "telegram_message_types_total",
    "Count of different message types",
    ["message_type"],  # text, voice, photo, etc.
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    await set_commands()
    await broker.connect()  # start broker connection
    await faststream_app.start()
    logger.debug("✅ Webhook set up")
    logger.debug("✅ Broker connected")

    yield

    # SHUTDOWN
    await bot.delete_webhook()
    await broker.close()
    await faststream_app.stop()
    print("❌ Webhook removed")
    print("❌ Broker disconnected")


app = FastAPI(title="Speech Coach API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instrumentation
Instrumentator().instrument(app).expose(app)


@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)

    # Track Telegram webhook requests separately
    if request.url.path == WEBHOOK_PATH:
        TELEGRAM_REQUESTS.labels(update_type="webhook").inc()
        TELEGRAM_REQUEST_LATENCY.labels(update_type="webhook").observe(
            time.time() - start_time
        )
    else:
        # Track other HTTP requests
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code,
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method, endpoint=request.url.path
        ).observe(time.time() - start_time)

    return response


@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    start_time = time.time()
    data = await request.json()
    update = Update.model_validate(data)

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
    TELEGRAM_REQUEST_LATENCY.labels(update_type=update_type).observe(
        time.time() - start_time
    )

    # Count message types
    if update.message:
        TELEGRAM_MESSAGE_TYPES.labels(message_type=update.message.content_type).inc()

    return {"ok": True}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
