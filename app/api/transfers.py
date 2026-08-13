import logging
from fastapi import APIRouter, Depends, HTTPException, Header, BackgroundTasks
from app.database import get_db

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.schemas import TransferRequest, TransferResponse
from app.services.services import create_transfer
from app.models.models import Account
from app.services.external.notification import send_notification
from app.services.external.ledger import update_ledger
from app.services.external.fraud import check_transfer
from app.services.errors import (
    NotFoundError,
    InsufficientFundsError,
    SameAccountError,
    CurrencyMismatchError,
    FraudDetectedError,
)
from app.api.auth import get_current_client

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/transfers", response_model=TransferResponse)
async def transfer(
    data: TransferRequest,
    background_tasks: BackgroundTasks,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    db: AsyncSession = Depends(get_db),
    current_client: int = Depends(get_current_client),
):
    try:
        # fraud check
        check = await check_transfer(data.from_account_id, data.to_account_id, data.amount)
        if not check:
            raise FraudDetectedError("Fraud detected")

        # owner check: ensure current client owns the source account
        q = await db.execute(select(Account).where(Account.id == data.from_account_id))
        sender = q.scalar_one_or_none()
        if sender is None:
            raise NotFoundError("Account not found")
        if sender.client_id != current_client:
            raise HTTPException(status_code=403, detail="Forbidden")

        result = await create_transfer(data, idempotency_key, db)
        background_tasks.add_task(send_notification, result.id)
        background_tasks.add_task(update_ledger, result.id)
        return result

    except (NotFoundError, InsufficientFundsError, SameAccountError, CurrencyMismatchError, FraudDetectedError) as e:
        logger.warning("Transfer failed: %s", str(e), extra={"from_account": data.from_account_id, "to_account": data.to_account_id})
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception:
        logger.exception("Transfer unexpected failure", extra={"from_account": data.from_account_id, "to_account": data.to_account_id})
        raise HTTPException(status_code=500, detail="Internal server error")