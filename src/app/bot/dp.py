from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from bot.handlers import question_handler, start_handler, voice_handler
from bot.middlewares.auth_middleware import AuthMiddleware
from bot.middlewares.database_session_middleware import DatabaseSessionMiddleware
from bot.middlewares.user_data_middleware import UserDataMiddleware

from config import settings

session = AiohttpSession()

bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    session=session,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML, protect_content=True),
)

dp = Dispatcher()
dp.message.middleware(DatabaseSessionMiddleware())
dp.message.middleware(UserDataMiddleware())
dp.message.middleware(AuthMiddleware())
dp.include_router(start_handler.router)
dp.include_router(question_handler.router)
dp.include_router(voice_handler.router)


async def set_commands():
    commands = [
        BotCommand(command="start", description="Start"),
        BotCommand(command="question", description="Get a question"),
    ]
    await bot.set_my_commands(commands)
