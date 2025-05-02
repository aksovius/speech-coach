from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from server.models.schema import UserQuota


async def get_user_quota(user_id: int, db: AsyncSession) -> UserQuota | None:
    result = await db.execute(select(UserQuota).where(user_id == user_id))
    user = result.scalar_one_or_none()
    return user


async def create_user_quota(user_id, db: AsyncSession) -> UserQuota:
    quota = UserQuota(user_id=user_id)
    db.add(quota)
    await db.commit()
    await db.refresh(quota)
    return quota
