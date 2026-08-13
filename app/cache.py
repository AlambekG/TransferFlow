import redis.asyncio as redis
from app.config import settings


redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=True
)

# TTL (seconds) used by cache callers
CACHE_TTL = settings.redis_ttl