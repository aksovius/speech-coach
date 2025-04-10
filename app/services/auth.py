from sqlalchemy.ext.asyncio import AsyncSession
from models.schema import User
from crud import user as crud_user, user_quota
from schemas.user import UserCreate

async def create_user(db: AsyncSession, user: UserCreate)-> User:
    user = await crud_user.create_user(db, user)
    await user_quota.create_user_quota(db, user.id)
    return user
async def get_current_user(db: AsyncSession, telegram_id: int) -> User:
    user = await crud_user.get_by_telegram_id(db, telegram_id)
    if not user:
        raise Exception("User not found")
    return user