from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db

from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import AccountResponse
from app.services.services import get_client_accounts, seed_database
from app.api.auth import get_current_client

router = APIRouter()



@router.get('/init')
async def init_seeed(db: AsyncSession = Depends(get_db)):
    try:
        await seed_database(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Seeding failed")


@router.get("/clients/{client_id}/accounts", response_model=list[AccountResponse])
async def get_accounts(
    client_id: int,
    db: AsyncSession = Depends(get_db),
    current_client: int = Depends(get_current_client),
):
    # owner-scoped: only allow client to read their own accounts
    if current_client != client_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    accounts = await get_client_accounts(
        client_id,
        db
    )
    return accounts