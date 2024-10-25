import os
from os import getenv

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.models.models import Language
from app.models.models import Movie, Director, Genre, Writer, Actor, Country, Rating
from app.schemans import MovieSchema

DATABASE_URL = os.getenv('DATABASE_URL')
async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db():
    async with async_session() as session:
        yield session



