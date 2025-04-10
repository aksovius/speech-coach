from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any

from schemas.user_schema import UserCreate
from services.auth_service import get_user_quota
from utils.database import with_db_session
ALLOWED_USERS = {1096190825}

class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Any],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        bot = data['bot']
        if not user:
            await bot.send_message("⛔Неизвестный пользователь.")
            return
        user_dto = UserCreate(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        user_quota = await with_db_session(get_user_quota, user_dto)
        print(f"🔑 user_quota: {user_quota}")

        #TODO: Delete on production
        if user and user.id not in ALLOWED_USERS:
            print(f"⛔ Доступ запрещён для user_id={user.id}")
            bot = data['bot']
            await bot.send_message(user.id, "⛔ У вас нет доступа к этому боту.")
            return


        if user_quota <= 0:
            print(f"⛔ Доступ запрещён для user_id={user.id}")
            await bot.send_message(user.id, "⛔ У вас закончились вопросы.")
            return

        return await handler(event, data)
