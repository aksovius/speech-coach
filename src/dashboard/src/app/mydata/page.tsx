import { headers } from 'next/headers';
import { validateTelegramWebAppData, parseTelegramInitData } from '@/lib/telegram';
import { getUserData } from '@/api/user';
import ChartCard from '@/components/ChartCard';

export default async function MyData({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined }
}) {

  const userData = await getUserData(searchParams);
  console.log('User data response:', userData);

  return (
    <>
        <ChartCard data={userData?.chart_data} stats={userData?.session} />

    <div>
      DEBUG
      <div className="text-gray-600">
        {userData?.user ? (
          <div>
            <p>ID: {userData.user.id}</p>
            <p>Имя: {userData.user.first_name}</p>
            {userData.user.last_name && <p>Фамилия: {userData.user.last_name}</p>}
            {userData.user.username && <p>Username: @{userData.user.username}</p>}
          </div>
        ) : (
          <div>Данные пользователя не найдены</div>
        )}
      </div>
    </div>
        </>
  );
}
