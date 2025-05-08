from typing import Optional

from clickhouse_driver import Client

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


async def get_session_stats(user_id: Optional[int], db=None):
    """
    Get overall statistics for user sessions
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
    return dict(zip(columns, result[0][0])) if result[0] else None


async def get_chart_data(user_id: Optional[int], db=None):
    """
    Get daily statistics for chart visualization
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
    return [dict(zip(columns, row)) for row in result[0]]
