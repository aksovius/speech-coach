import { getTelegramHeaders } from '../utils/telegram';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function getUserData(searchParams: { [key: string]: string | string[] | undefined }) {
  console.log('SSR Debug - API URL:', API_URL);
  const query = new URLSearchParams();

  for (const key in searchParams) {
    const value = searchParams[key];
    if (typeof value === 'string') {
      query.append(key, value);
    }
  }

  try {
    const url = `${API_URL}/api/statistics?${query.toString()}`;
    console.log('SSR Debug - Request URL:', url);

    // Get Telegram headers if available
    const telegramHeaders = getTelegramHeaders();
    console.log('SSR Debug - Telegram Headers:', telegramHeaders);

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...telegramHeaders, // Add Telegram headers
    };

    const response = await fetch(url, {
      next: { revalidate: 60 }, // Cache for 60 seconds
      headers,
    });

    console.log('SSR Debug - Response status:', response.status);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('SSR Debug - Response data:', data);

    return data;
  } catch (error: any) {
    console.error('SSR Debug - Error details:', {
      message: error?.message,
      stack: error?.stack,
      cause: error?.cause
    });

    return {
      total_sessions: 0,
      avg_ttr: 0,
      avg_score: 0,
      first_session: null,
      last_session: null
    };
  }
}
