from fastapi import FastAPI

from app.database import engine
from app.models import Base, Account, Client, Transfer
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(app.api.router)
app.include_router(app.monitoring.router)
