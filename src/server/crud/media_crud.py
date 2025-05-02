from sqlalchemy.ext.asyncio import AsyncSession

from server.models.schema import Media


async def save_media(media: Media, db: AsyncSession) -> None:
    db.add(media)
    await db.commit()
    await db.refresh(media)
    return
