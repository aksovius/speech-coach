from faststream.redis import RedisBroker

from config import settings

broker = RedisBroker(settings.REDIS_URL)
