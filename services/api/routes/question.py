from fastapi import APIRouter, Depends
from pydantic import BaseModel
from services.question import generate_question
from crud.question import save_user_question
from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/question", tags=["Question"])

class QuestionRequest(BaseModel):
    user_id: int

class QuestionResponse(BaseModel):
    question: str

@router.post("", response_model=QuestionResponse)
async def create_question(data: QuestionRequest, db: AsyncSession = Depends(get_db)):
    question = await generate_question()
    await save_user_question(db, user_id=data.user_id, question=question)
    return {"question": question}
