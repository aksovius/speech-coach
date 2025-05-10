import { getSessionStats, getChartData } from '../queries/stats';

interface Stats {
  total_sessions: number;
  avg_ttr: number;
  avg_score: number;
  first_session: string;
  last_session: string;
}

interface ChartData {
  date: string;
  avg_ttr: number;
  avg_score: number;
  attempts: number;
}

export default async function Home() {
  const [sessionStats, chartData] = await Promise.all([
    getSessionStats(),
    getChartData(),
  ]) as [Stats, ChartData[]];

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-8">Statistics</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <div className="p-4 border rounded-lg">
            <h2 className="text-xl font-semibold mb-4">Session Overview</h2>
            <p>Total Sessions: {sessionStats.total_sessions}</p>
            <p>Average TTR: {sessionStats.avg_ttr.toFixed(2)}</p>
            <p>Average Score: {sessionStats.avg_score.toFixed(2)}</p>
            <p>First Session: {new Date(sessionStats.first_session).toLocaleDateString()}</p>
            <p>Last Session: {new Date(sessionStats.last_session).toLocaleDateString()}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-4">
          <div className="p-4 border rounded-lg">
            <h2 className="text-xl font-semibold mb-4">Daily Progress</h2>
            <div className="space-y-2">
              {chartData.map((day) => (
                <div key={day.date} className="flex justify-between">
                  <span>{new Date(day.date).toLocaleDateString()}</span>
                  <span>TTR: {day.avg_ttr.toFixed(2)}</span>
                  <span>Score: {day.avg_score.toFixed(2)}</span>
                  <span>Attempts: {day.attempts}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
