from faststream.redis import RedisBroker

from shared.config import settings

# Initialize Redis broker with settings
broker = RedisBroker(
    url=settings.REDIS_URL,
    # # Enable automatic decoding of responses
    # decode_responses=True,
    # # Enable retries on timeout
    # retry_on_timeout=True,
    # # Set connection timeout
    # socket_timeout=5.0,
    # # Set connection pool settings
    # max_connections=10,
    # # Enable health checks
    # health_check_interval=30,
)
