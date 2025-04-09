from models.schema import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    return user

async def create_user(db: AsyncSession, telegram_id: int, user_name: str | None = None, first_name: str | None = None, last_name: str | None = None) -> User:
    user = User(telegram_id=telegram_id, user_name=user_name, first_name=first_name, last_name=last_name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_by_telegram_id(db: AsyncSession, telegram_id: int) -> User | None:
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    return user