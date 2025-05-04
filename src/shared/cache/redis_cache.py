import redis

from shared.config import settings

# Initialize Redis client for caching
redis_cache = redis.Redis.from_url(settings.REDIS_CACHE_URL)
