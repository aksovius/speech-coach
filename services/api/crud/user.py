from typing import Optional

from models.schema import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from schemas.user import UserCreate


async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    return user

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    user = User(telegram_id=user.telegram_id, username=user.username, first_name=user.first_name, last_name=user.last_name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_by_telegram_id(db: AsyncSession, telegram_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    return user