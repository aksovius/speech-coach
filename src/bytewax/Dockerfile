FROM python:3.11-slim-bullseye
WORKDIR /bytewax
COPY ./requirements.txt /bytewax/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED 1
