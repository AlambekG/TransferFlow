import pytest


from tests.test_app import create_test_accounts


@pytest.mark.asyncio
async def test_transfer_blocked_on_fraud(client, monkeypatch):
    # simulate fraud detector returning False
    async def fake_check(from_id, to_id, amount):
        return False

    monkeypatch.setattr("app.services.external.fraud.check_transfer", fake_check)

    sender_id, receiver_id = await create_test_accounts()

    response = await client.post(
        "/transfers",
        headers={
            "Idempotency-Key": "fraud-block-test"
        },
        json={
            "from_account_id": sender_id,
            "to_account_id": receiver_id,
            "amount": 10
        }
    )

    assert response.status_code == 400
    assert "Fraud detected" in response.json()["detail"]
