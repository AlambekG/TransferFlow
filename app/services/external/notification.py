import asyncio
from app.services.retries import retry
from app.services.circuit_breaker import CircuitBreaker

breaker = CircuitBreaker()


@breaker.call
@retry(3)
async def send_notification(data):
    """ mock notification service """
    await asyncio.sleep(0.3)
    print(
        f"Notification sent for transfer {data}"
    )