from models.schema import UserAnswer
from sqlalchemy.ext.asyncio import AsyncSession


async def save_answer(answer: UserAnswer, db: AsyncSession) -> None:
    db.add(answer)
    await db.commit()
    await db.refresh(answer)
    return
