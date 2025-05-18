# async def get_current_user(
#     telegram_id: int,
#     db: AsyncSession = Depends(get_db),
# ) -> User:
#     user = await auth.get_user_by_telegram_id(db, telegram_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# async def get_or_create_user(
#     db: AsyncSession = Depends(get_db),
#     user: User = Depends(get_current_user),
# ) -> User:
#     return await auth.get_or_create_user_by_telegram_id(db, user)

from typing import Optional
from urllib.parse import parse_qsl

from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from server.utils.database import get_db
from server.utils.telegram import parse_telegram_user_data, validate_telegram_data
from shared.config import settings
from shared.schemas.user_schema import UserCreate
from shared.services.auth_service import get_user_id_and_quota


async def get_user_id_and_quota_dependency(
    telegram_data: dict,
    db: AsyncSession = Depends(get_db),
):
    """
    Dependency to get user_id and quota from telegram data.
    Can be used in routes with query parameters from Telegram WebApp.
    """
    if not validate_telegram_data(
        telegram_data.copy(), bot_token=settings.TELEGRAM_BOT_TOKEN
    ):
        raise HTTPException(status_code=400, detail="Invalid signature")

    user_data = parse_telegram_user_data(telegram_data.get("user"))
    if not user_data:
        raise HTTPException(status_code=400, detail="Invalid user data")

    user_dto = UserCreate(
        telegram_id=user_data.get("id"),
        first_name=user_data.get("first_name", ""),
        last_name=user_data.get("last_name", ""),
        username=user_data.get("username", ""),
    )

    return await get_user_id_and_quota(user_dto, db)


async def get_user_with_quota(
    request: Optional[Request] = None,
    telegram_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Universal dependency that works with both:
    1. WebApp requests with telegram data in query parameters
    2. Direct API calls with telegram_id parameter

    Returns dict with user_id and quota
    """
    if request and not telegram_id:
        # Case 1: WebApp request with telegram data
        raw_query = request.url.query
        parsed = dict(parse_qsl(raw_query, keep_blank_values=True))
        return await get_user_id_and_quota_dependency(parsed, db)

    elif telegram_id:
        # Case 2: Direct API call with telegram_id
        user_dto = UserCreate(
            telegram_id=telegram_id, first_name="", last_name="", username=""
        )
        return await get_user_id_and_quota(user_dto, db)

    else:
        raise HTTPException(
            status_code=400, detail="Either request or telegram_id must be provided"
        )
