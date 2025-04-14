from models.schema import Question, UserQuestionHistory
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
from sqlalchemy import select, insert




async def get_unseen_questions(user_id: int, db: AsyncSession):
    #TODO: move to crud layer
    subquery = select(UserQuestionHistory.question_id).where(UserQuestionHistory.user_id == user_id)
    result = await db.execute(
        select(Question).where(Question.id.not_in(subquery)).limit(1)
    )
    question = result.scalars().first()
    if not question:
        return None  # или выбросить исключение

    # Запись истории
    await db.execute(
        insert(UserQuestionHistory).values(user_id=user_id, question_id=question.id)
    )
    await db.commit()

    return question.text