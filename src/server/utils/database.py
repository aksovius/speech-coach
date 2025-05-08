from sqlalchemy.ext.asyncio import AsyncSession

from server.database import async_session


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


async def with_db_session(func, *args, **kwargs):
    async with async_session() as session:
        return await func(*args, db=session, **kwargs)
