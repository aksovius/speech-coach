from typing import Any, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from schemas.user_schema import UserCreate


class UserDataMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Any],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        bot = data["bot"]
        if not user:
            await bot.send_message("⛔ Unknown user.")
            return

        user_dto = UserCreate(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )

        data["user_dto"] = user_dto
        return await handler(event, data)
