import pytest
import asyncio
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import AsyncSessionLocal
from app.models import Account, Client, Transfer
from sqlalchemy import delete
from app.cache import redis_client

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

@pytest_asyncio.fixture(autouse=True)
async def _close_redis():
    yield
    await redis_client.connection_pool.disconnect()

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

