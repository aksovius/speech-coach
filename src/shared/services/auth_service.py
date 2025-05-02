from server.crud import user_crud as crud_user
from server.crud import user_quota_crud
from server.models.schema import User
from shared.schemas.user_schema import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession

# async def create_user(db: AsyncSession, user: UserCreate)-> User:
#     user = await crud_user.create_user(db, user)
#     await user_quota_crud.create_user_quota(user.id, db)
#     return user
# async def get_current_user(telegram_id: int, db: AsyncSession) -> User | None:
#     user = await crud_user.get_by_telegram_id(db, telegram_id)
#     if not user:
#         return None
#     return user


async def get_current_user_or_create(user_dto: UserCreate, db: AsyncSession) -> User:
    user = await crud_user.get_by_telegram_id(user_dto.telegram_id, db)
    if not user:
        user = await crud_user.create_user(user_dto, db)
        await user_quota_crud.create_user_quota(user.id, db)
    return user


async def get_user_id_and_quota(user_dto: UserCreate, db: AsyncSession) -> dict:
    user = await get_current_user_or_create(user_dto=user_dto, db=db)
    user_quota = await user_quota_crud.get_user_quota(user.id, db)
    return {"user_id": user.id, "quota": user_quota.total_allowed - user_quota.used}
