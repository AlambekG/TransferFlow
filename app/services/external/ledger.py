import asyncio
from app.services.retries import retry
from app.services.circuit_breaker import CircuitBreaker

breaker = CircuitBreaker()


@breaker.call
@retry(3)
async def update_ledger(data):
    """ mock ledger function """
    await asyncio.sleep(0.3)
    print(
        f"Ledger updated for transfer {data}"
    )