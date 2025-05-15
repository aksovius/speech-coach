import crypto from 'crypto';

interface TelegramInitData {
  query_id?: string;
  user?: {
    id: number;
    first_name: string;
    last_name?: string;
    username?: string;
    language_code?: string;
  };
  auth_date: number;
  hash: string;
}

export function validateTelegramWebAppData(initData: string, botToken: string): boolean {
  try {
    const urlParams = new URLSearchParams(initData);
    const hash = urlParams.get('hash');
    if (!hash) return false;

    // Удаляем hash из параметров
    urlParams.delete('hash');

    // Сортируем параметры
    const params: string[] = [];
    urlParams.forEach((value, key) => {
      params.push(`${key}=${value}`);
    });
    params.sort();

    // Создаем строку для проверки
    const dataCheckString = params.join('\n');

    // Создаем секретный ключ
    const secretKey = crypto.createHmac('sha256', 'WebAppData')
      .update(botToken)
      .digest();

    // Вычисляем хеш
    const calculatedHash = crypto.createHmac('sha256', secretKey)
      .update(dataCheckString)
      .digest('hex');

    return calculatedHash === hash;
  } catch (error) {
    console.error('Error validating Telegram WebApp data:', error);
    return false;
  }
}

export function parseTelegramInitData(initData: string): TelegramInitData | null {
  try {
    const urlParams = new URLSearchParams(initData);
    const userStr = urlParams.get('user');

    return {
      query_id: urlParams.get('query_id') || undefined,
      user: userStr ? JSON.parse(userStr) : undefined,
      auth_date: parseInt(urlParams.get('auth_date') || '0'),
      hash: urlParams.get('hash') || ''
    };
  } catch (error) {
    console.error('Error parsing Telegram init data:', error);
    return null;
  }
}
