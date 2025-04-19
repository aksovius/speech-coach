from dependencies import get_db
from fastapi import APIRouter, Depends
from schemas.question_schema import QuestionRequest, QuestionResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/question", tags=["Question"])


@router.get("", response_model=QuestionResponse)
async def get_question(user: QuestionRequest, db: AsyncSession = Depends(get_db)):
    return await question.get_question_for_user(user=user, db=db)


# @router.post("", response_model=QuestionResponse)
# async def create_question(data: QuestionRequest, db: AsyncSession = Depends(get_db)):
#     question = await generate_question()
#     await save_user_question(db, user_id=data.user_id, question=question)
#     return {"question": question}
