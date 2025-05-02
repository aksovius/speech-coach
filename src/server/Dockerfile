FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY src/server/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
ENV PYTHONPATH=/app/src

COPY . .

CMD ["uvicorn", "src.server.main:app", "--host", "0.0.0.0", "--port", "8000"]
