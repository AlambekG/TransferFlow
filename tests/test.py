import pytest


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