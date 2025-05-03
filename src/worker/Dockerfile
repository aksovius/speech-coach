FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /src
ENV PYTHONPATH=/src

COPY src/worker/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/worker /src/worker
COPY src/shared /src/shared

CMD ["python", "-m", "worker.main"]
