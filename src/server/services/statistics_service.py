from typing import List, Optional

from server.crud.clickhouse_crud import (
    get_daily_statistics,
    get_session_statistics,
    get_word_cloud_data,
)
from server.models.statistics import DailyStatistics, SessionStatistics, WordCloudItem


async def get_session_stats(user_id: Optional[int]) -> Optional[SessionStatistics]:
    """
    Get overall statistics for user sessions
    """
    return await get_session_statistics(user_id)


async def get_chart_data(user_id: Optional[int]) -> List[DailyStatistics]:
    """
    Get daily statistics for chart visualization
    """
    return await get_daily_statistics(user_id)


async def get_word_cloud(user_id: Optional[int]) -> List[WordCloudItem]:
    """
    Get word cloud data for visualization
    """
    return await get_word_cloud_data(user_id)
