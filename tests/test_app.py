import pytest

@pytest.mark.asyncio
async def test_something():
    assert True

@pytest.mark.asyncio
async def test_get_accounts(client):

    response = await client.get(
        "/clients/1/accounts"
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

    response = await client.post(
        "/transfers",
        headers={
            "Idempotency-Key": "test-transfer-1"
        },
        json={
            "from_account_id": 1,
            "to_account_id": 3,
            "amount": 100
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "COMPLETED"


@pytest.mark.asyncio
async def test_transfer_idempotency(client):

    headers = {
        "Idempotency-Key": "duplicate-test"
    }

    payload = {
        "from_account_id": 1,
        "to_account_id": 3,
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

    response = await client.post(
        "/transfers",
        headers={
            "Idempotency-Key": "insufficient-balance-test"
        },
        json={
            "from_account_id": 3,
            "to_account_id": 1,
            "amount": 999999
        }
    )

    assert response.status_code == 400
    assert "Insufficient balance" in response.json()["detail"]


@pytest.mark.asyncio
async def test_transfer_same_account(client):

    response = await client.post(
        "/transfers",
        headers={
            "Idempotency-Key": "same-account-test"
        },
        json={
            "from_account_id": 1,
            "to_account_id": 1,
            "amount": 100
        }
    )

    assert response.status_code == 400
    assert "Cannot transfer to same account" in response.json()["detail"]