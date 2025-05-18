import { headers } from 'next/headers';
import { validateTelegramWebAppData, parseTelegramInitData } from '@/lib/telegram';
import { getUserData } from '@/api/user';

export default async function MyData({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined }
}) {
  console.log('searchParams', searchParams);
  const headersList = headers();
  console.log('All headers:', Object.fromEntries(headersList.entries()));

  const userData = await getUserData(searchParams);
  console.log('User data response:', userData);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-gray-600">
        {userData?.user ? (
          <div>
            <h1 className="text-2xl font-bold mb-4">Данные пользователя</h1>
            <p>ID: {userData.user.id}</p>
            <p>Имя: {userData.user.first_name}</p>
            {userData.user.last_name && <p>Фамилия: {userData.user.last_name}</p>}
            {userData.user.username && <p>Username: @{userData.user.username}</p>}
          </div>
        ) : (
          <div>Данные пользователя не найдены</div>
        )}
      </div>
    </main>
  );
}
