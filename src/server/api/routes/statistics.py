from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from server.services.statistics_service import get_chart_data, get_session_stats
from server.utils.database import get_db

router = APIRouter(prefix="/api/statistics", tags=["Statistics"])


class StatisticsResponse(BaseModel):
    total_sessions: int
    avg_ttr: float
    avg_score: float
    first_session: datetime
    last_session: datetime


class ChartDataResponse(BaseModel):
    date: datetime
    avg_ttr: float
    avg_score: float
    attempts: int


@router.get("/sessions", response_model=StatisticsResponse)
async def get_statistics(
    user_id: Optional[int] = None, db: AsyncSession = Depends(get_db)
):
    """
    Get overall statistics for user sessions
    """
    return await get_session_stats(user_id, db)


@router.get("/chart", response_model=list[ChartDataResponse])
async def get_statistics_chart(
    user_id: Optional[int] = None, db: AsyncSession = Depends(get_db)
):
    """
    Get daily statistics for chart visualization
    """
    return await get_chart_data(user_id, db)


# @router.post("", response_model=QuestionResponse)
# async def create_question(data: QuestionRequest, db: AsyncSession = Depends(get_db)):
#     question = await generate_question()
#     await save_user_question(db, user_id=data.user_id, question=question)
#     return {"question": question}
