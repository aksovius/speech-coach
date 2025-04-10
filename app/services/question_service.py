from crud import question_crud
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.question_schema import QuestionRequest

async def get_question_for_user(user: QuestionRequest, db: AsyncSession):
    
    return await question_crud.get_unseen_questions(db, user)