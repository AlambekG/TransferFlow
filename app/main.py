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

@app.get("/health")
def liveness_check():
    """
    checks if the app is running.
    """
    return {
        "status": "alive",
    }

@app.get('/')
def read():
    return "Hello World"

@app.get('/clients/accounts')
def getAccounts():
    ...

@app.post('/transfers')
def transfer():
    ...