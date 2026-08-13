import asyncio
from app.services.retries import retry
from app.services.circuit_breaker import CircuitBreaker

# Protect external mock with a circuit breaker to avoid repeated calls when failing
breaker = CircuitBreaker()


@breaker.call
@retry(3)
async def check_transfer(from_id, to_id, amount):
    """ mock fraud detection. currently just return true"""
    await asyncio.sleep(0.3)
    return True