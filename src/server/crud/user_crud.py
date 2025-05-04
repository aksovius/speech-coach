import json
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.schema import User
from shared.cache.redis_cache import redis_cache
from shared.schemas.user_schema import UserCreate


async def get_user(user_id: int, db: AsyncSession) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    return user


async def create_user(user: UserCreate, db: AsyncSession) -> User:
    user = User(
        telegram_id=user.telegram_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


def get_cached_user(telegram_id: int) -> User | None:
    """
    Get user from cache by telegram_id

    Args:
        telegram_id (int): Telegram user ID

    Returns:
        User | None: User object from cache or None if not found
    """
    data = redis_cache.get(f"user:{telegram_id}")
    if data:
        user_dict = json.loads(data)
        return User(**user_dict)
    return None


def set_cached_user(telegram_id: int, user: User, expire_seconds: int = 3600):
    """
    Save user to cache

    Args:
        telegram_id (int): Telegram user ID
        user (User): User object to cache
        expire_seconds (int): Cache expiration time in seconds (default: 1 hour)
    """
    user_dict = {
        "id": user.id,
        "telegram_id": user.telegram_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }
    redis_cache.setex(f"user:{telegram_id}", expire_seconds, json.dumps(user_dict))


async def get_by_telegram_id(telegram_id: int, db: AsyncSession) -> Optional[User]:
    """
    Get user by telegram_id with cache support

    Args:
        telegram_id (int): Telegram user ID
        db (AsyncSession): Database session

    Returns:
        Optional[User]: User object or None if not found
    """
    # Try to get from cache first
    cached_user = get_cached_user(telegram_id)
    if cached_user:
        return cached_user
    # If not in cache, get from database
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()

    # If found in database, cache it
    if user:
        set_cached_user(telegram_id, user)

    return user
