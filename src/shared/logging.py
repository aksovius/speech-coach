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
            "event": getattr(record, "event", "unknown"),
        }

        # Add extra fields if present
        if hasattr(record, "extra"):
            log_data.update(record.extra)

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
            "event": getattr(record, "event", "unknown"),
        }

        # Add extra fields if present
        if hasattr(record, "extra"):
            log_data.update(record.extra)

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
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create stdout handler
    handler = logging.StreamHandler()
    handler.setFormatter(LokiFormatter() if use_loki else JSONFormatter())
    logger.addHandler(handler)

    # Add additional attributes to log records
    logger = logging.LoggerAdapter(logger, {"service": service, "component": component})

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
