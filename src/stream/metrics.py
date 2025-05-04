from prometheus_client import Counter, Histogram, start_http_server

# Общие метрики для всех workflow'ов
PROCESSED_MESSAGES = Counter(
    "processed_messages_total",
    "Total number of processed messages",
    ["workflow", "status"],
)

PROCESSING_LATENCY = Histogram(
    "message_processing_seconds", "Time spent processing messages", ["workflow", "step"]
)

ERRORS = Counter(
    "processing_errors_total",
    "Total number of processing errors",
    ["workflow", "error_type"],
)


def start_metrics_server(port: int = 9090, path: str = "/metrics"):
    """Запускает HTTP сервер для метрик Prometheus"""
    start_http_server(port, addr="0.0.0.0")
