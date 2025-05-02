from sqlalchemy.ext.asyncio import AsyncSession

from server.models.schema import UserAnswer


async def save_answer(answer: UserAnswer, db: AsyncSession) -> int:
    db.add(answer)
    await db.commit()
    await db.refresh(answer)
    return answer.id
