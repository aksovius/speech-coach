import time

from fastapi import Request

from ..metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    TELEGRAM_REQUEST_LATENCY,
    TELEGRAM_REQUESTS,
)

WEBHOOK_PATH = "/webhook"


async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)

    # Track Telegram webhook requests separately
    if request.url.path == WEBHOOK_PATH:
        TELEGRAM_REQUESTS.labels(update_type="webhook").inc()
        TELEGRAM_REQUEST_LATENCY.labels(update_type="webhook").observe(
            time.time() - start_time
        )
    else:
        # Track other HTTP requests
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code,
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method, endpoint=request.url.path
        ).observe(time.time() - start_time)

    return response
