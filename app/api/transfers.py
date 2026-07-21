import logging
from fastapi import APIRouter, Depends, HTTPException, Header, BackgroundTasks
from app.database import get_db

from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import TransferRequest, TransferResponse
from app.services.services import create_transfer

from app.services.external.notification import send_notification
from app.services.external.ledger import update_ledger
from app.services.external.fraud import check_transfer

router = APIRouter()
logger = logging.getLogger(__name__)

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
        # await kafka.publish(
        #     "transfer-events",
        #     {
        #         "transfer_id": result.id
        #     }
        # )
        background_tasks.add_task(
            update_ledger,
            result.id
        )
        return result

    except Exception as e:
        logger.exception(
            "Transfer failed",
            extra={
                "from_account": data.from_account_id,
                "to_account": data.to_account_id,
                "amount": str(data.amount)
            }
        )
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )