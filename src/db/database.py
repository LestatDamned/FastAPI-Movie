from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.config import settings

async_engine = create_async_engine(settings.database_url, echo=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db():
    async with async_session() as session:
        yield session
