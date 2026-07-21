from fastapi import FastAPI

from app.database import engine
from app.models.models import Base, Account, Client, Transfer
from contextlib import asynccontextmanager
from app.api.api import router as apiRouter
from app.monitoring import router as monitoringRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(apiRouter)
app.include_router(monitoringRouter)
