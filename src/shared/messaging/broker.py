from faststream.redis import RedisBroker
from shared.config import settings

broker = RedisBroker(settings.REDIS_URL)
