import clickhouse from '../lib/clickhouse';

export async function getSessionStats(userId?: number) {
  const whereClause = userId ? `WHERE user_id = ${userId}` : '';

  const query = `
    SELECT
      count() as total_sessions,
      avg(ttr) as avg_ttr,
      avg(score_overall) as avg_score,
      min(timestamp) as first_session,
      max(timestamp) as last_session
    FROM speech.answer_ttr
    ${whereClause}
  `;

  const result = await clickhouse.query({
    query,
    format: 'JSONEachRow',
  });

  return result.json();
}

export async function getChartData(userId?: number) {
  const whereClause = userId ? `WHERE user_id = ${userId}` : '';

  const query = `
    SELECT
      toStartOfDay(timestamp) as date,
      avg(ttr) as avg_ttr,
      avg(score_overall) as avg_score,
      count() as attempts
    FROM speech.answer_ttr
    ${whereClause}
    GROUP BY date
    ORDER BY date ASC
  `;

  const result = await clickhouse.query({
    query,
    format: 'JSONEachRow',
  });

  return result.json();
}
