import ChartCard from '@/components/ChartCard';
import WordCloudCard from '@/components/WordCloudCard';
import { getSessionStats, getChartData } from '@/queries/stats';
import { ChartData, Stats } from '@/types/stats';

export default async function Home() {
  const [sessionStats, chartData] = await Promise.all([
    getSessionStats(),
    getChartData(),
  ]) as [Stats[], ChartData[]];

  const stats = sessionStats[0] || {
    total_sessions: 0,
    avg_ttr: 0,
    avg_score: 0,
    first_session: null,
    last_session: null
  };

  return (
    <div className="space-y-6">
      <header className="space-y-2">
        <h1 className="text-3xl font-bold text-gray-900">Speech Coach Dashboard</h1>
        <p className="text-lg text-gray-600">Track your progress and vocabulary</p>
      </header>

      <ChartCard data={chartData} stats={stats} />
      <WordCloudCard />
    </div>
  );
}
