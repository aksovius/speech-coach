#!/bin/bash
set -e

echo "Migrating database..."
alembic upgrade head

echo "Starting application..."
exec gunicorn -k uvicorn.workers.UvicornWorker services.api.main:app --bind 0.0.0.0:8000
