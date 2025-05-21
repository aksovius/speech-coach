from datetime import datetime
from urllib.parse import parse_qsl

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from server.services.statistics_service import (
    get_chart_data,
    get_session_stats,
    get_word_cloud,
)
from server.utils.database import get_db
from server.utils.telegram import parse_telegram_user_data, validate_telegram_data
from shared.config import settings
from shared.services.auth_service import get_user_id_by_telegram_id

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


@router.get("/")
async def get_statistics(request: Request, db: AsyncSession = Depends(get_db)):
    raw_query = request.url.query
    print("raw_query", raw_query)
    parsed = dict(parse_qsl(raw_query, keep_blank_values=True))

    if not validate_telegram_data(parsed.copy(), bot_token=settings.TELEGRAM_BOT_TOKEN):
        raise HTTPException(status_code=400, detail="Invalid signature")

    telegram_data = parse_telegram_user_data(parsed.get("user"))

    if not telegram_data:
        raise HTTPException(status_code=400, detail="Invalid user data")

    user_id = await get_user_id_by_telegram_id(
        telegram_id=telegram_data.get("id"), db=db
    )
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid user data")

    session = await get_session_stats(user_id=user_id)
    chart_data = await get_chart_data(user_id=user_id)
    word_cloud = await get_word_cloud(user_id=user_id)
    print("chart_data", chart_data)
    print("session", session)
    return {
        "status": "success",
        "user": telegram_data,
        "session": session,
        "chart_data": chart_data,
        "word_cloud": word_cloud,
    }
