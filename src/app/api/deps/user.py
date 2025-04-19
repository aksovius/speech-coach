from dependencies import get_db
from fastapi import Depends, HTTPException
from models.schema import User
from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_user(
    telegram_id: int,
    db: AsyncSession = Depends(get_db),
) -> User:
    user = await auth.get_user_by_telegram_id(db, telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_or_create_user(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> User:
    return await auth.get_or_create_user_by_telegram_id(db, user)
