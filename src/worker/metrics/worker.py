from prometheus_client import Counter, Histogram

# Worker Processing Metrics
PROCESSED_MESSAGES = Counter(
    "worker_processed_messages_total",
    "Total number of processed messages",
    ["message_type"],  # audio, text, etc.
)

PROCESSING_LATENCY = Histogram(
    "worker_processing_duration_seconds",
    "Time spent processing messages",
    ["message_type"],
)

PROCESSING_ERRORS = Counter(
    "worker_processing_errors_total",
    "Total number of processing errors",
    ["message_type", "error_type"],
)
