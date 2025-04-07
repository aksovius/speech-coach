from models.question import Question
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def save_user_question(db: AsyncSession, user_id: int, question: str):
    q = Question(user_id=user_id, text=question)
    db.add(q)
    await db.commit()
