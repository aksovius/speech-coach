import crypto from 'crypto';

export function verifyTelegramInitData(initData: string, botToken: string): boolean {
  try {
    const urlParams = new URLSearchParams(initData);
    const hash = urlParams.get('hash');
    urlParams.delete('hash');

    // Сортируем параметры по алфавиту
    const params: [string, string][] = [];
    urlParams.forEach((value, key) => {
      params.push([key, value]);
    });
    params.sort(([a], [b]) => a.localeCompare(b));

    // Создаем строку для проверки
    const checkString = params
      .map(([key, value]) => `${key}=${value}`)
      .join('\n');

    // Создаем секретный ключ
    const secretKey = crypto
      .createHmac('sha256', 'WebAppData')
      .update(botToken)
      .digest();

    // Вычисляем хеш
    const calculatedHash = crypto
      .createHmac('sha256', secretKey)
      .update(checkString)
      .digest('hex');

    return calculatedHash === hash;
  } catch (error) {
    console.error('Error verifying Telegram init data:', error);
    return false;
  }
}
