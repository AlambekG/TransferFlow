import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Account, Client, Transfer, TransferStatusEnum
from app.cache import redis_client
from decimal import Decimal

async def get_client_accounts(
    client_id: int,
    db: AsyncSession
):
    cache_key = f"client:{client_id}:accounts"
    cached = await redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    result = await db.execute(
        select(Account)
        .where(Account.client_id == client_id)
    )

    accounts = result.scalars().all()
    response = [
        {
            "id": account.id,
            "balance": str(account.balance),
            "currency": account.currency
        }
        for account in accounts
    ]

    await redis_client.set(
        cache_key,
        json.dumps(response),
        ex=300
    )

    return response


async def seed_database(db: AsyncSession):
    result = await db.execute(
        select(Client)
    )
    clients = result.scalars().all()

    if clients:
        return

    client1 = Client(
        full_name="John Doe",
        email="john@example.com"
    )

    client2 = Client(
        full_name="Alice Smith",
        email="alice@example.com"
    )

    db.add_all([client1, client2])

    await db.flush()

    accounts = [
        Account(
            client_id=client1.id,
            balance=1000,
            currency="USD"
        ),
        Account(
            client_id=client1.id,
            balance=500,
            currency="EUR"
        ),
        Account(
            client_id=client2.id,
            balance=200,
            currency="USD"
        )
    ]

    db.add_all(accounts)

    await db.commit()


async def create_transfer(data, idempotency_key: str, db: AsyncSession):
    if data.from_account_id == data.to_account_id:
        raise Exception("Cannot transfer to same account")
    amount = Decimal(str(data.amount))

    async with db.begin():
        existing = await db.execute(
            select(Transfer)
            .where(
                Transfer.idempotency_key == idempotency_key
            )
        )
        existing_transfer = existing.scalar_one_or_none()

        if existing_transfer:
            return existing_transfer
        
        result = await db.execute(
            select(Account)
            .where(
                Account.id.in_(
                    [
                        data.from_account_id,
                        data.to_account_id
                    ]
                )
            )
            .with_for_update()
        )
        accounts = result.scalars().all()
        if len(accounts) != 2:
            raise Exception(
                "Account not found"
            )
        sender = next(
            a for a in accounts
            if a.id == data.from_account_id
        )
        receiver = next(
            a for a in accounts
            if a.id == data.to_account_id
        )
        if sender.balance < data.amount:
            raise Exception(
                "Insufficient balance"
            )

        sender.balance -= data.amount
        receiver.balance += data.amount

        transfer = Transfer(
            idempotency_key=idempotency_key,
            from_account_id=sender.id,
            to_account_id=receiver.id,
            amount=data.amount,
            status=TransferStatusEnum.COMPLETED
        )
        db.add(transfer)
    await db.refresh(transfer)

    await redis_client.delete(
        f"client:{data.from_account_id}:accounts"
    )
    await redis_client.delete(
        f"client:{data.to_account_id}:accounts"
    )
    
    return transfer