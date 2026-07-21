import pytest
from app.cache import redis_client

from app.database import AsyncSessionLocal
from app.models.models import Client, Account, Transfer
from sqlalchemy import delete



async def clear_database():
    async with AsyncSessionLocal() as session:
        await session.execute(delete(Transfer))
        await session.execute(delete(Account))
        await session.execute(delete(Client))
        await session.commit()

async def clear_cache():
    await redis_client.flushdb()


async def create_test_accounts():
    async with AsyncSessionLocal() as db:
        await db.execute(delete(Transfer))
        await db.execute(delete(Account))
        await db.execute(delete(Client))
        await db.commit()

        sender_client = Client(
            full_name="Sender",
            email="sender@test.com"
        )

        receiver_client = Client(
            full_name="Receiver",
            email="receiver@test.com"
        )

        db.add_all([
            sender_client,
            receiver_client
        ])

        await db.flush()

        sender = Account(
            client_id=sender_client.id,
            balance=1000,
            currency="USD"
        )

        receiver = Account(
            client_id=receiver_client.id,
            balance=500,
            currency="USD"
        )

        db.add_all([
            sender,
            receiver
        ])

        await db.commit()

        return sender.id, receiver.id


@pytest.mark.asyncio
async def test_get_accounts(client):
    sender_id, receiver_id = await create_test_accounts()

    response = await client.get(
        f"/clients/{sender_id}/accounts"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0
    assert "currency" in data[0]
    assert "balance" in data[0]

@pytest.mark.asyncio
async def test_transfer_account_not_found(client):
    response = await client.post(
        "/transfers",
        headers={
            "Idempotency-Key": "account-not-found-test"
        },
        json={
            "from_account_id": 999,
            "to_account_id": 3,
            "amount": 100
        }
    )

    assert response.status_code == 400
    assert "Account not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_transfer_success(client):
    sender_id, receiver_id = await create_test_accounts()

    response = await client.post(
        "/transfers",
        headers={
            "Idempotency-Key": "test-transfer-2"
        },
        json={
            "from_account_id": sender_id,
            "to_account_id": receiver_id,
            "amount": 100
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "completed"


@pytest.mark.asyncio
async def test_transfer_idempotency(client):
    sender_id, receiver_id = await create_test_accounts()
    headers = {
        "Idempotency-Key": "duplicate-test"
    }

    payload = {
        "from_account_id": sender_id,
        "to_account_id": receiver_id,
        "amount": 50
    }


    first = await client.post(
        "/transfers",
        headers=headers,
        json=payload
    )

    second = await client.post(
        "/transfers",
        headers=headers,
        json=payload
    )


    assert first.json()["id"] == second.json()["id"]

@pytest.mark.asyncio
async def test_transfer_insufficient_balance(client):
    sender_id, receiver_id = await create_test_accounts()
    response = await client.post(
        "/transfers",
        headers={
            "Idempotency-Key": "insufficient-balance-test"
        },
        json={
            "from_account_id": sender_id,
            "to_account_id": receiver_id,
            "amount": 999999
        }
    )

    assert response.status_code == 400
    assert "Insufficient balance" in response.json()["detail"]


@pytest.mark.asyncio
async def test_transfer_same_account(client):
    sender_id, receiver_id = await create_test_accounts()

    response = await client.post(
        "/transfers",
        headers={
            "Idempotency-Key": "same-account-test"
        },
        json={
            "from_account_id": sender_id,
            "to_account_id": sender_id,
            "amount": 100
        }
    )

    assert response.status_code == 400
    assert "Cannot transfer to same account" in response.json()["detail"]

@pytest.mark.asyncio
async def test_accounts_redis_cache(client):
    sender_id, receiver_id = await create_test_accounts()
    cache_key = f"client:{sender_id}:accounts"
    await redis_client.delete(cache_key)

    response = await client.get(f"/clients/{sender_id}/accounts")
    assert response.status_code == 200
    cached = await redis_client.get(cache_key)
    assert cached is not None