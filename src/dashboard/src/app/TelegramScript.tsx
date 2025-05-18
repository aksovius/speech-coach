'use client';

import Script from "next/script";

export default function TelegramScript() {
  return (
    <Script
      src="https://telegram.org/js/telegram-web-app.js"
      strategy="afterInteractive"
      onLoad={() => {
        console.log('Telegram WebApp script loaded');
        if (window.Telegram?.WebApp) {
          console.log('Initializing Telegram WebApp');
          window.Telegram.WebApp.ready();
          if (!window.location.pathname.includes('/mydata')) {
            const params = new URLSearchParams(window.Telegram.WebApp.initData);
            const url = `/mydata?${params}`;
            console.log('Redirecting to:', url);
            window.location.href = url;
          } else {
            console.log('Already on /mydata page');
          }
        }
      }}
    />
  );
}
