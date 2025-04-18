from aiogram.types import Update
from bot.dp import bot, dp, set_commands
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.messaging.broker import broker
import app.messaging.consumers  
from config import settings

WEBHOOK_PATH = f"/webhook/{settings.TELEGRAM_BOT_TOKEN}"
WEBHOOK_URL = f"https://aksovius.ddns.net{WEBHOOK_PATH}"

app = FastAPI(title="Speech Coach API", version="0.1.0")

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


@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    await set_commands()
    await broker.start()
    print("✅ Webhook установлен")
    print("✅ Брокер подключён")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()
    await broker.close()
    print("🛑 Webhook удалён")
    print("🛑 Брокер отключён")