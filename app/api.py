from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db

from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import AccountResponse, TransferRequest, TransferResponse
from app.services import get_client_accounts, create_transfer

router = APIRouter()


@router.get("/clients/{client_id}/accounts", response_model=list[AccountResponse])
async def get_accounts(client_id: int, db: AsyncSession = Depends(get_db)):
    accounts = await get_client_accounts(
        client_id,
        db
    )
    return accounts


@router.post(
    "/transfers",
    response_model=TransferResponse
)
async def transfer(data: TransferRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = await create_transfer(
            data,
            db
        )
        return result

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )