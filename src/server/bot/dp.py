from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from server.bot.handlers import (
    architecture_handler,
    question_handler,
    start_handler,
    statistics_handler,
    toefl_handler,
    voice_handler,
)
from server.bot.middlewares.auth_middleware import AuthMiddleware
from server.bot.middlewares.database_session_middleware import DatabaseSessionMiddleware
from server.bot.middlewares.user_data_middleware import UserDataMiddleware
from shared.config import settings

session = AiohttpSession()

bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    session=session,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML, protect_content=True),
)

dp = Dispatcher()

# Register middleware for messages
dp.message.middleware(DatabaseSessionMiddleware())
dp.message.middleware(UserDataMiddleware())
dp.message.middleware(AuthMiddleware())

# Register middleware for callback queries
dp.callback_query.middleware(DatabaseSessionMiddleware())
dp.callback_query.middleware(UserDataMiddleware())
dp.callback_query.middleware(AuthMiddleware())

# Register routers
dp.include_router(start_handler.router)
dp.include_router(toefl_handler.router)
dp.include_router(question_handler.router)
dp.include_router(voice_handler.router)
dp.include_router(statistics_handler.router)
dp.include_router(architecture_handler.router)


async def set_commands():
    commands = [
        BotCommand(command="start", description="Start"),
        BotCommand(command="statistics", description="Statistics"),
        # BotCommand(command="question", description="Get a question"),
    ]
    await bot.set_my_commands(commands)
