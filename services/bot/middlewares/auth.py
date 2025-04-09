from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any

ALLOWED_USERS = {1096190825}
BACKEND_URL = "http://localhost:8000"

class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Any],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        if user and user.id not in ALLOWED_USERS:
            print(f"⛔ Доступ запрещён для user_id={user.id}")
            bot = data['bot']
            await bot.send_message(user.id, "⛔ У вас нет доступа к этому боту.")
            return 

        return await handler(event, data)
