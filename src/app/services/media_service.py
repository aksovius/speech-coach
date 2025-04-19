from crud import media_crud
from models.schema import Media


async def save_media(media: Media, db):
    return await media_crud.save_media(media, db)
