import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.services import seed_database
from app.database import AsyncSessionLocal
from app.models import Account, Client, Transfer
from sqlalchemy import delete

async def clear_database():
    async with AsyncSessionLocal() as session:
        await session.execute(delete(Transfer))
        await session.execute(delete(Account))
        await session.execute(delete(Client))
        await session.commit()

@pytest.fixture
async def client():
    await clear_database()

    async with AsyncSessionLocal() as session:
        await seed_database(session)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
