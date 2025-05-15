from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import coalesce

from server.models.schema import Question, UserQuestionHistory


async def get_unseen_questions(
    user_id: int, db: AsyncSession, category: str = None
) -> Question | None:

    subquery = (
        select(UserQuestionHistory.question_id, func.count().label("ask_count"))
        .group_by(UserQuestionHistory.question_id)
        .subquery()
    )

    query = select(Question).outerjoin(subquery, Question.id == subquery.c.question_id)

    if category:
        query = query.where(Question.category == category)

    query = query.where(Question.is_active)

    query = query.order_by(coalesce(subquery.c.ask_count, 0), func.random()).limit(1)

    result = await db.execute(query)
    question = result.scalars().first()

    if question:
        await db.execute(
            insert(UserQuestionHistory).values(user_id=user_id, question_id=question.id)
        )
        await db.commit()
        return question

    return None
