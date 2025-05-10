import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
console.log('API_URL', API_URL);
export async function getSessionStats(userId?: number) {
  const response = await axios.get(`${API_URL}/api/statistics/sessions`, {
    params: { user_id: userId }
  });
  console.log('session stats', response);
  return response.data;
}

export async function getChartData(userId?: number) {
  const response = await axios.get(`${API_URL}/api/statistics/chart`, {
    params: { user_id: userId }
  });
  console.log('chart data', response);
  return response.data;
}
