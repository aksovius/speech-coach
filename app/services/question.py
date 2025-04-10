from crud import question
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.question import QuestionRequest

async def get_question_for_user(user: QuestionRequest, db: AsyncSession):
    
    return await question.get_unseen_questions(db, user)