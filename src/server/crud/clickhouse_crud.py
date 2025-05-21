from typing import List, Optional

from clickhouse_driver import Client

from server.models.statistics import DailyStatistics, SessionStatistics, WordCloudItem
from shared.config import settings


def get_clickhouse_client() -> Client:
    """
    Get ClickHouse client instance
    """
    return Client(
        host=settings.CLICKHOUSE_HOST,
        port=settings.CLICKHOUSE_PORT,
        user=settings.CLICKHOUSE_USER,
        password=settings.CLICKHOUSE_PASSWORD,
        database=settings.CLICKHOUSE_DATABASE,
    )


async def get_session_statistics(
    user_id: Optional[int] = None,
) -> Optional[SessionStatistics]:
    """
    Get raw session statistics from ClickHouse
    """
    where_clause = f"WHERE user_id = {user_id}" if user_id else ""

    query = f"""
        SELECT
            count() as total_sessions,
            avg(ttr) as avg_ttr,
            avg(score_overall) as avg_score,
            min(timestamp) as first_session,
            max(timestamp) as last_session
        FROM speech.answer_ttr
        {where_clause}
    """

    client = get_clickhouse_client()
    result = client.execute(query, with_column_types=True)
    columns = [col[0] for col in result[1]]
    if not result[0]:
        return None
    data = dict(zip(columns, result[0][0]))
    return SessionStatistics(**data)


async def get_daily_statistics(user_id: Optional[int] = None) -> List[DailyStatistics]:
    """
    Get raw daily statistics from ClickHouse
    """
    where_clause = f"WHERE user_id = {user_id}" if user_id else ""

    query = f"""
        SELECT
            toStartOfDay(timestamp) as date,
            avg(ttr) as avg_ttr,
            avg(score_overall) as avg_score,
            count() as attempts
        FROM speech.answer_ttr
        {where_clause}
        GROUP BY date
        ORDER BY date ASC
    """

    client = get_clickhouse_client()
    result = client.execute(query, with_column_types=True)
    columns = [col[0] for col in result[1]]
    return [DailyStatistics(**dict(zip(columns, row))) for row in result[0]]


async def get_word_cloud_data(user_id: Optional[int] = None) -> List[WordCloudItem]:
    """
    Get word cloud data from ClickHouse for the last month
    Returns list of top 15 WordCloudItem objects
    """
    where_clause = f"WHERE user_id = {user_id}" if user_id else ""
    time_filter = "AND timestamp >= now() - INTERVAL 1 MONTH"

    query = f"""
        SELECT
            word AS text,
            sum(word_count) AS value
        FROM speech.active_words
        {where_clause}
        {time_filter}
        GROUP BY word
        ORDER BY value DESC
        LIMIT 30
    """

    client = get_clickhouse_client()
    result = client.execute(query, with_column_types=True)
    columns = [col[0] for col in result[1]]
    return [WordCloudItem(**dict(zip(columns, row))) for row in result[0]]
