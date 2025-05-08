import json
import logging
from datetime import datetime
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """Formatter for JSON log output"""

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "service": getattr(record, "service", "unknown"),
            "component": getattr(record, "component", "unknown"),
        }

        # Add all extra fields that might be stored on the record
        excluded_keys = [
            "args",
            "exc_info",
            "exc_text",
            "levelname",
            "msecs",
            "msg",
            "message",
            "name",
            "pathname",
            "process",
            "processName",
            "relativeCreated",
            "thread",
            "threadName",
            "asctime",
            "created",
            "filename",
            "funcName",
            "levelno",
            "lineno",
            "module",
            "service",
            "component",
        ]

        for key, value in record.__dict__.items():
            if key not in excluded_keys and not key.startswith("_"):
                log_data[key] = value

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


class LokiFormatter(logging.Formatter):
    """Formatter for Loki-compatible JSON log output"""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "service": getattr(record, "service", "unknown"),
            "component": getattr(record, "component", "unknown"),
        }

        # Add all extra fields that might be stored on the record
        excluded_keys = [
            "args",
            "exc_info",
            "exc_text",
            "levelname",
            "msecs",
            "msg",
            "message",
            "name",
            "pathname",
            "process",
            "processName",
            "relativeCreated",
            "thread",
            "threadName",
            "asctime",
            "created",
            "filename",
            "funcName",
            "levelno",
            "lineno",
            "module",
            "service",
            "component",
        ]

        for key, value in record.__dict__.items():
            if key not in excluded_keys and not key.startswith("_"):
                log_data[key] = value

        return json.dumps(log_data)


def setup_logger(
    name: str,
    level: int = logging.INFO,
    service: str = "unknown",
    component: str = "unknown",
    use_loki: bool = False,
) -> logging.Logger:
    """
    Configure logger with JSON formatting

    Args:
        name: Logger name
        level: Logging level
        service: Service name
        component: Component name
        use_loki: Whether to use Loki formatter
    """

    class ContextFilter(logging.Filter):
        """Filter that adds context to log records"""

        def __init__(self, service, component):
            super().__init__()
            self.service = service
            self.component = component

        def filter(self, record):
            record.service = self.service
            record.component = self.component
            return True

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers and filters
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    for filter in logger.filters[:]:
        logger.removeFilter(filter)

    # Add a context filter to inject service and component
    context_filter = ContextFilter(service, component)
    logger.addFilter(context_filter)

    # Create stdout handler
    handler = logging.StreamHandler()
    handler.setFormatter(LokiFormatter() if use_loki else JSONFormatter())
    logger.addHandler(handler)

    return logger


# Predefined log levels
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def get_log_level(level_name: str) -> int:
    """Get logging level by name"""
    return LOG_LEVELS.get(level_name.upper(), logging.INFO)
