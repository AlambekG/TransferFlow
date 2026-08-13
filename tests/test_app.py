import pytest
from decimal import Decimal
from app.cache import redis_client

from app.database import AsyncSessionLocal
from app.models.models import Client, Account, Transfer
from sqlalchemy import delete, select



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

        return sender_client.id, receiver_client.id, sender.id, receiver.id


@pytest.mark.asyncio
async def test_get_accounts(client):
    client_sender_id, client_receiver_id, sender_account_id, receiver_account_id = await create_test_accounts()

    response = await client.get(
        f"/clients/{client_sender_id}/accounts",
        headers={"X-Client-Id": str(client_sender_id)}
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
            "Idempotency-Key": "account-not-found-test",
            "X-Client-Id": "1",
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
    client_sender_id, client_receiver_id, sender_id, receiver_id = await create_test_accounts()
    # prime cache entries to verify invalidation
    from_key = f"client:{client_sender_id}:accounts"
    to_key = f"client:{client_receiver_id}:accounts"
    await redis_client.set(from_key, "x")
    await redis_client.set(to_key, "y")

    response = await client.post(
        "/transfers",
        headers={
            "Idempotency-Key": "test-transfer-2",
            "X-Client-Id": str(client_sender_id),
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

    # verify DB state: balances adjusted and transfer recorded
    transfer_id = data["id"]
    async with AsyncSessionLocal() as session:
        tr = await session.get(Transfer, transfer_id)
        assert tr is not None
        assert tr.amount == Decimal("100")
        assert tr.idempotency_key == "test-transfer-2"

        sender = await session.get(Account, sender_id)
        receiver = await session.get(Account, receiver_id)
        assert sender.balance == Decimal("900")
        assert receiver.balance == Decimal("600")

    # cache keys should be invalidated
    assert await redis_client.get(from_key) is None
    assert await redis_client.get(to_key) is None


@pytest.mark.asyncio
async def test_transfer_idempotency(client):
    client_sender_id, client_receiver_id, sender_id, receiver_id = await create_test_accounts()
    headers = {
        "Idempotency-Key": "duplicate-test",
        "X-Client-Id": str(client_sender_id),
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
    # ensure only one transfer record exists and balances reflect a single deduction
    async with AsyncSessionLocal() as session:
        # Query to count transfers with the idempotency key
        result = await session.execute(
            select(Transfer).where(Transfer.idempotency_key == "duplicate-test")
        )
        transfers = result.scalars().all()
        assert len(transfers) == 1

        sender = await session.get(Account, sender_id)
        receiver = await session.get(Account, receiver_id)
        # initial sender balance 1000, amount 50 -> 950
        assert sender.balance == Decimal("950")
        assert receiver.balance == Decimal("550")

@pytest.mark.asyncio
async def test_transfer_insufficient_balance(client):
    client_sender_id, client_receiver_id, sender_id, receiver_id = await create_test_accounts()
    response = await client.post(
        "/transfers",
        headers={
            "Idempotency-Key": "insufficient-balance-test",
            "X-Client-Id": str(client_sender_id),
        },
        json={
            "from_account_id": sender_id,
            "to_account_id": receiver_id,
            "amount": 999999
        }
    )

    assert response.status_code == 400
    assert "Insufficient balance" in response.json()["detail"]
    # ensure no transfer record created and balances unchanged
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Transfer).where(Transfer.idempotency_key == "insufficient-balance-test")
        )
        transfers = result.scalars().all()
        assert len(transfers) == 0

        sender = await session.get(Account, sender_id)
        receiver = await session.get(Account, receiver_id)
        assert sender.balance == Decimal("1000")
        assert receiver.balance == Decimal("500")


@pytest.mark.asyncio
async def test_transfer_same_account(client):
    client_sender_id, client_receiver_id, sender_id, receiver_id = await create_test_accounts()

    response = await client.post(
        "/transfers",
        headers={
            "Idempotency-Key": "same-account-test",
            "X-Client-Id": str(client_sender_id),
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
    client_sender_id, client_receiver_id, sender_id, receiver_id = await create_test_accounts()
    cache_key = f"client:{client_sender_id}:accounts"
    await redis_client.delete(cache_key)

    response = await client.get(f"/clients/{client_sender_id}/accounts", headers={"X-Client-Id": str(client_sender_id)})
    assert response.status_code == 200
    cached = await redis_client.get(cache_key)
    assert cached is not None