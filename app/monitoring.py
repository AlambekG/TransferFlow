from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.future import select

router = APIRouter()

@router.get("/health")
def liveness_check():
    """
    checks if the app is running.
    """
    return {
        "status": "alive",
    }


async def verify_db_readiness(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(select(text("1")))
    except Exception as e:
        print(f"db readiness check failed: {e}")
        raise HTTPException(status_code=503, detail=f"database is not ready: {e}")
    return True


@router.get("/ready")
async def readiness_check(_: bool = Depends(verify_db_readiness)):
    """
    checks if the app is ready.
    if verify_db_readiness fails, exception will be thrown.
    """
    return {"status": "ready"}


@router.get('/')
def read():
    return "Hello World"

