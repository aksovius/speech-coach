FROM python:3.11-slim-bullseye
WORKDIR /src
COPY ./src/stream/requirements.txt /src/stream/requirements.txt
RUN pip install --no-cache-dir -r stream/requirements.txt

ENV PYTHONUNBUFFERED 1
