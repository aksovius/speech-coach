export interface ChartData {
  date: string;
  avg_ttr: number;
  avg_score: number;
  attempts: number;
}

export interface Stats {
  total_sessions: number;
  avg_ttr: number;
  avg_score: number;
  first_session: string | null;
  last_session: string | null;
}
