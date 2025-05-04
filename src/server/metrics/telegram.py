from prometheus_client import Counter, Histogram

# Telegram Bot Metrics
TELEGRAM_REQUESTS = Counter(
    "telegram_requests_total",
    "Total number of Telegram bot requests",
    ["update_type"],  # message, callback_query, etc.
)

TELEGRAM_REQUEST_LATENCY = Histogram(
    "telegram_request_duration_seconds",
    "Time spent processing Telegram requests",
    ["update_type"],
)

TELEGRAM_MESSAGE_TYPES = Counter(
    "telegram_message_types_total",
    "Count of different message types",
    ["message_type"],  # text, voice, photo, etc.
)
