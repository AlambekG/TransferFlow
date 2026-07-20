from fastapi import APIRouter, Depends, HTTPException, Header, BackgroundTasks
from app.database import get_db

from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import AccountResponse, TransferRequest, TransferResponse
from app.services import get_client_accounts, create_transfer

from app.external.notification import send_notification
from app.external.ledger import update_ledger
from app.external.fraud import check_transfer

router = APIRouter()


@router.get("/clients/{client_id}/accounts", response_model=list[AccountResponse])
async def get_accounts(client_id: int, db: AsyncSession = Depends(get_db)):
    accounts = await get_client_accounts(
        client_id,
        db
    )
    return accounts


@router.post("/transfers", response_model=TransferResponse)
async def transfer(
    data: TransferRequest, 
    background_tasks: BackgroundTasks,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    db: AsyncSession = Depends(get_db)
):
    try:
        check = await check_transfer(data.from_account_id, data.to_account_id, data.amount)
        if not check:
            raise Exception("Fraud detected")
     
        result = await create_transfer(data, idempotency_key, db)
        background_tasks.add_task(
            send_notification,
            result.id
        )
        background_tasks.add_task(
            update_ledger,
            result.id
        )
        return result

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )