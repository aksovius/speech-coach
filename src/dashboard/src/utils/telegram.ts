// Check if we're in Telegram Web App
export const isTelegramWebApp = () => {
  // Проверяем, что мы на клиенте
  if (typeof window === 'undefined') {
    console.log('Debug - Server-side rendering, window is not available');
    return false;
  }

  console.log('Debug - Window object:', typeof window);
  console.log('Debug - Telegram object:', window?.Telegram);
  console.log('Debug - WebApp object:', window?.Telegram?.WebApp);
  return typeof window !== 'undefined' && window.Telegram?.WebApp;
};

// Get user data from Telegram Web App
export const getTelegramUser = () => {
  if (!isTelegramWebApp()) {
    console.log('Debug - Not in Telegram Web App');
    return null;
  }
  try {
    const initData = window.Telegram?.WebApp?.initData;
    const user = window.Telegram?.WebApp?.initDataUnsafe?.user;
    console.log('Debug - Telegram initData:', initData);
    console.log('Debug - Telegram user:', user);
    return user || null;
  } catch (error) {
    console.error('Error getting Telegram user:', error);
    return null;
  }
};

// Get headers with Telegram user data
export const getTelegramHeaders = (): Record<string, string> => {
  // На сервере возвращаем пустой объект
  if (typeof window === 'undefined') {
    console.log('Debug - Server-side rendering, returning empty headers');
    return {};
  }

  const user = getTelegramUser();
  console.log('Debug - User from getTelegramUser:', user);
  if (!user) return {};

  return {
    'X-Telegram-User-ID': user.id.toString(),
    'X-Telegram-Username': user.username || '',
    'X-Telegram-First-Name': user.first_name || '',
    'X-Telegram-Last-Name': user.last_name || '',
  };
};
