FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /src
ENV PYTHONPATH=/src

COPY src/server/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/server /src/server
COPY src/shared /src/shared

# CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
