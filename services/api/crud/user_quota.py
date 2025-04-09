from models.schema import UserQuota
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def get_user_quota(db: AsyncSession, user_id: int) -> UserQuota | None:
    result = await db.execute(select(UserQuota).where(user_id == user_id))
    user = result.scalar_one_or_none()
    return user

async def create_user_quota(db: AsyncSession, user_id) -> UserQuota:
    quota = UserQuota(user_id=user_id)
    db.add(quota)
    await db.commit()
    await db.refresh(quota)
    return quota