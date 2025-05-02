from sqlalchemy.ext.asyncio import AsyncSession

from server.crud import question_crud


async def get_question_for_user(user_id: int, db: AsyncSession):

    return await question_crud.get_unseen_questions(user_id, db)
