from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.config import settings

# Use configured database URL (reads from env or .env via pydantic-settings)
DATABASE_URL = settings.database_url

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session