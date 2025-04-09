import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import TELEGRAM_BOT_TOKEN
from handlers import start, question, voice
from middlewares.auth import AuthMiddleware
from aiogram.types import BotCommand

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начать"),
        BotCommand(command="question", description="Получить вопрос"),
    ]
    await bot.set_my_commands(commands)
    
async def main():
    session = AiohttpSession()
    bot = Bot(
    token=TELEGRAM_BOT_TOKEN,
    session=session,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        protect_content=True
    )
)
    dp = Dispatcher()

    dp.message.middleware(AuthMiddleware())
    
    dp.include_router(start.router)
    dp.include_router(question.router)
    dp.include_router(voice.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("🤖 Бот запущен и слушает сообщения...")
    asyncio.run(main())