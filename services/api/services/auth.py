from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from crud import user as crud_user, quota as crud_quota


async def create_user(db: AsyncSession, user: UserCreate)-> User:
    user = await crud_user.create_user(db, telegram_id=user.telegram_id, user_name=user.user_name, first_name=user.first_name, last_name=user.last_name)
    await crud_quota.create_user_quota(db, user_id=user.id, total_allowed=INITIAL_FREE_QUOTA)
    return user