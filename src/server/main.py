import logging
from contextlib import asynccontextmanager

import server.consumers.audio_consumer  # noqa: F401   !DO NOT REMOVE
from aiogram.types import Update
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from faststream import FastStream
from server.bot.dp import bot, dp, set_commands
from shared.config import settings
from shared.messaging.broker import broker

logger = logging.getLogger(__name__)
WEBHOOK_PATH = f"/webhook/{settings.TELEGRAM_BOT_TOKEN}"
WEBHOOK_URL = f"https://{settings.APP_HOST}{WEBHOOK_PATH}"
faststream_app = FastStream(
    broker
)  # Create a FastStream app with the broker (resiver app)


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

# app.include_router(question.router)
# app.include_router(user.router)


@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}
