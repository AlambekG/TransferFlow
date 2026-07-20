from fastapi import APIRouter, Depends, Request, Response, status
from app.database import get_db

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get('/clients/{client_id}/accounts')
async def get_accounts(
    client_id: int,
    db: AsyncSession = Depends(get_db)
):
    ...


@router.post('/transfers')
def transfer():
    ...

async def seed():
    ...