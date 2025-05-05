'use client';

import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { ChartData, Stats } from '@/types/stats';

interface ChartCardProps {
  data: ChartData[];
  stats: Stats;
}

export default function ChartCard({ data, stats }: ChartCardProps) {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!data || data.length === 0) {
    return (
      <div className="rounded-lg bg-white p-4 shadow-sm">
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Progress</h2>
        <div className="h-[300px] w-full flex items-center justify-center text-gray-500">
          No data available
        </div>
      </div>
    );
  }

  if (!isMounted) {
    return (
      <div className="rounded-lg bg-white p-4 shadow-sm">
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Progress</h2>
        <div className="h-[300px] w-full flex items-center justify-center text-gray-500">
          Loading...
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-lg bg-white p-4 shadow-sm">
      <div className="mb-3 grid grid-cols-3 gap-4 border-b border-gray-100 pb-3">
        <div>
          <p className="text-sm text-gray-600">Total Answers</p>
          <p className="text-xl font-bold text-gray-900">{stats.total_sessions}</p>
        </div>
        <div>
          <p className="text-sm text-gray-600">Average TTR</p>
          <p className="text-xl font-bold text-gray-900">{stats.avg_ttr.toFixed(2)}</p>
        </div>
        <div>
          <p className="text-sm text-gray-600">Average Score</p>
          <p className="text-xl font-bold text-gray-900">{Math.round(stats.avg_score)}</p>
        </div>
      </div>

      <h2 className="text-lg font-semibold text-gray-900 mb-2">Progress</h2>
      <div className="h-[300px] w-full" style={{ minHeight: '300px', position: 'relative' }}>
        <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0 }}>
          <ResponsiveContainer>
            <LineChart
              data={data}
              margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="date"
                tickFormatter={(date) => new Date(date).toLocaleDateString('en-US', { day: 'numeric', month: 'short' })}
                tick={{ fontSize: 11 }}
                height={50}
              />
              <YAxis
                yAxisId="left"
                orientation="left"
                stroke="#8884d8"
                tick={{ fontSize: 11 }}
                width={50}
              />
              <YAxis
                yAxisId="right"
                orientation="right"
                stroke="#82ca9d"
                tick={{ fontSize: 11 }}
                width={50}
              />
              <Tooltip
                labelFormatter={(date) => new Date(date).toLocaleDateString('en-US', {
                  day: 'numeric',
                  month: 'long',
                  year: 'numeric'
                })}
                formatter={(value: number, name: string) => {
                  if (name === 'TTR') return [value.toFixed(2), name];
                  if (name === 'Score') return [Math.round(value), name];
                  return [value, name];
                }}
                contentStyle={{
                  backgroundColor: 'white',
                  border: '1px solid #ccc',
                  borderRadius: '4px',
                  padding: '6px'
                }}
              />
              <Legend />
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="avg_ttr"
                name="TTR"
                stroke="#8884d8"
                strokeWidth={2}
                dot={{ r: 3 }}
                activeDot={{ r: 4 }}
              />
              <Line
                yAxisId="right"
                type="monotone"
                dataKey="avg_score"
                name="Score"
                stroke="#82ca9d"
                strokeWidth={2}
                dot={{ r: 3 }}
                activeDot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
