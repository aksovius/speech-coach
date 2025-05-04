import os
from typing import Any, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from shared.logging import get_log_level, setup_logger
from shared.services.auth_service import get_user_id_and_quota

# Configure logger with Loki formatter
logger = setup_logger(
    name="server.bot.auth",
    level=get_log_level(os.getenv("LOG_LEVEL", "INFO")),
    service=os.getenv("LOG_SERVICE", "speech-coach"),
    component="server.bot.auth",
    use_loki=True,
)

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
        logger.info(
            "User authentication check",
            extra={
                "event": "auth_check",
                "telegram_id": user_dto.telegram_id,
                "quota": user_data["quota"],
                "user_id": user_data["user_id"],
            },
        )

        # TODO: Delete on production
        if user_dto.telegram_id not in ALLOWED_USERS:
            logger.warning(
                "Access denied - user not in allowed list",
                extra={
                    "event": "access_denied",
                    "telegram_id": user_dto.telegram_id,
                    "reason": "not_allowed_user",
                },
            )
            await bot.send_message(user_dto.username, "⛔ Access denied to this bot.")
            return

        if user_data["quota"] <= 0:
            logger.warning(
                "Access denied - no quota left",
                extra={
                    "event": "access_denied",
                    "telegram_id": user_dto.telegram_id,
                    "reason": "no_quota",
                },
            )
            await bot.send_message(user_dto.username, "⛔ You have no questions left.")
            return

        data["user_id"] = user_data["user_id"]
        logger.info(
            "User authenticated successfully",
            extra={
                "event": "auth_success",
                "telegram_id": user_dto.telegram_id,
                "user_id": user_data["user_id"],
            },
        )
        return await handler(event, data)
