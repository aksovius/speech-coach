from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand

from config import settings
from bot.middlewares.auth_middleware import AuthMiddleware
from bot.handlers import start_handler, question_handler, voice_handler

session = AiohttpSession()

bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    session=session,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        protect_content=True
    )
)

dp = Dispatcher()
dp.message.middleware(AuthMiddleware())
dp.include_router(start_handler.router)
dp.include_router(question_handler.router)
dp.include_router(voice_handler.router)

async def set_commands():
    commands = [
        BotCommand(command="start", description="Начать"),
        BotCommand(command="question", description="Получить вопрос"),
    ]
    await bot.set_my_commands(commands)
