from models.schema import Question, UserQuestionHistory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def save_user_question(db: AsyncSession, user_id: int, question: str):
    q = Question(user_id=user_id, text=question)
    db.add(q)
    await db.commit()


async def get_unseen_questions(db: AsyncSession, user_id: int):
    subquery = select(UserQuestionHistory.question_id).where(UserQuestionHistory.user_id == user_id)
    result = await db.execute(
        select(Question).where(Question.id.not_in(subquery)).limit(1)
    )
    return result.scalars().first()