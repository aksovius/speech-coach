from models.schema import Question, UserQuestionHistory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert




async def get_unseen_questions(user_id: int, db: AsyncSession) -> Question | None:
    # TODO: move to crud layer

    # Get unseen questions for the user
    subquery = select(UserQuestionHistory.question_id).where(UserQuestionHistory.user_id == user_id)

    # Take the first unseen question
    result = await db.execute(
        select(Question).where(Question.id.not_in(subquery)).limit(1)
    )
    question = result.scalars().first()

    # If there are unseen questions, add to history
    if question:
        await db.execute(
            insert(UserQuestionHistory).values(user_id=user_id, question_id=question.id)
        )
        await db.commit()
        return question

    # Get the last seen question for the user
    result = await db.execute(
        select(Question)
        .join(UserQuestionHistory, Question.id == UserQuestionHistory.question_id)
        .where(UserQuestionHistory.user_id == user_id)
        .order_by(UserQuestionHistory.assigned_at.desc())
        .limit(1)
    )
    seen_question = result.scalars().first()
    if seen_question:
        # If there are no unseen questions, return the last seen question
        await db.execute(
            insert(UserQuestionHistory).values(user_id=user_id, question_id=seen_question.id)
        )
        await db.commit()
        return seen_question
    return None
