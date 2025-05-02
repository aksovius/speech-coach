from typing import Any, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from shared.services.auth_service import get_user_id_and_quota

ALLOWED_USERS = {1096190825}


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Any],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user_dto = data.get("user_dto")
        bot = data["bot"]
        db = data["db"]
        user_data = await get_user_id_and_quota(user_dto, db)
        print(f"🔑 user_quota: {user_data}")

        # TODO: Delete on production
        if user_dto.telegram_id not in ALLOWED_USERS:
            print(f"⛔ Access denied for user_id={user_dto.telegram_id}")
            await bot.send_message(user_dto.username, "⛔ Access denied to this bot.")
            return

        if user_data["quota"] <= 0:
            print(f"⛔ Access denied for user_id={user_dto.telegram_id}")
            await bot.send_message(user_dto.username, "⛔ You have no questions left.")
            return
        data["user_id"] = user_data["user_id"]
        return await handler(event, data)
