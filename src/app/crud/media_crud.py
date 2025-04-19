from models.schema import Media
from sqlalchemy.ext.asyncio import AsyncSession


async def save_media(media: Media, db: AsyncSession) -> None:
    db.add(media)
    await db.commit()
    await db.refresh(media)
    return
