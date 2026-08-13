import asyncio
import logging
from functools import wraps
from app.config import settings


logger = logging.getLogger(__name__)


def retry(retries=None, delay=None):
    """Decorator for retrying async operations. Defaults come from settings when not provided."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            r = retries if retries is not None else settings.retry_retries
            d = delay if delay is not None else settings.retry_delay
            for attempt in range(r):
                try:
                    return await func(*args, **kwargs)
                except Exception:
                    logger.warning(
                        "External service failed, retrying",
                        extra={
                            "attempt": attempt + 1,
                            "service": func.__name__
                        }
                    )
                    if attempt == r - 1:
                        raise
                    await asyncio.sleep(
                        d * (2 ** attempt)
                    )
        return wrapper
    return decorator