# Используем официальный образ Python
FROM python:3.11-slim

# Установка зависимостей для pydub и ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Создание рабочей директории
WORKDIR /app

# Копируем исходный код в контейнер
COPY . .

# Открываем порт, если ты планируешь использовать webhook (иначе можно убрать)
EXPOSE 8080

# Устанавливаем переменные окружения (если нужно)
ENV PYTHONUNBUFFERED=1

# Запускаем бота
# CMD ["python", "main.py"]
