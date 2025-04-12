from models.schema import Question, UserQuestionHistory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select




async def get_unseen_questions(user_id: int, db: AsyncSession):
    subquery = select(UserQuestionHistory.question_id).where(UserQuestionHistory.user_id == user_id)
    result = await db.execute(
        select(Question).where(Question.id.not_in(subquery)).limit(1)
    )
    return result.scalars().first()