from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand

from bot.middlewares.database_session_middleware import DatabaseSessionMiddleware
from bot.middlewares.user_data_middleware import UserDataMiddleware
from config import settings
from bot.middlewares.auth_middleware import AuthMiddleware
from bot.handlers import start_handler, question_handler, voice_handler

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
session = AiohttpSession()

bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    session=session,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        protect_content=True
    )
)

class CustomDataMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        print("Middleware triggered!")  # Отладочный вывод
        data["custom_key"] = "custom_value"
        print("Data in middleware:", data)
        return await handler(event, data)
dp = Dispatcher()
dp.message.middleware(CustomDataMiddleware())
# dp.message.middleware(DatabaseSessionMiddleware())
# dp.message.middleware(UserDataMiddleware())
# dp.message.middleware(AuthMiddleware())
dp.include_router(start_handler.router)
dp.include_router(question_handler.router)
dp.include_router(voice_handler.router)

async def set_commands():
    commands = [
        BotCommand(command="start", description="Начать"),
        BotCommand(command="question", description="Получить вопрос"),
    ]
    await bot.set_my_commands(commands)
