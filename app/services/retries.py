import asyncio
import logging
from functools import wraps


logger = logging.getLogger(__name__)

def retry(retries=3, delay=0.5):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(retries):
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
                    if attempt == retries - 1:
                        raise
                    await asyncio.sleep(
                        delay * (2 ** attempt)
                    )
        return wrapper
    return decorator