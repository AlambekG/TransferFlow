from fastapi import APIRouter, Depends
from app.database import get_db

from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import AccountResponse
from app.services.services import get_client_accounts, seed_database

router = APIRouter()


@router.get('/init')
async def init_seeed(db: AsyncSession = Depends(get_db)):
    try:
        await seed_database(db)
    except Exception as e:
        raise Exception(f'Seeding failed {e}')


@router.get("/clients/{client_id}/accounts", response_model=list[AccountResponse])
async def get_accounts(client_id: int, db: AsyncSession = Depends(get_db)):
    accounts = await get_client_accounts(
        client_id,
        db
    )
    return accounts