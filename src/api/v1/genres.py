from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.tables import Genre

router = APIRouter()


@router.get("/genres/")
async def get_genre(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Genre))
    genres = result.scalars().all()
    return genres


@router.get("/genres/{genre_id}/")
async def get_genre(genre_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Genre).filter_by(id=genre_id))
    genres = result.scalar_one_or_none()
    return genres


@router.patch("/genres/{genre_id}/")
async def update_genre(genre_id: int, new_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Genre).filter_by(id=genre_id))
    genre = result.scalar_one_or_none()
    if genre is None:
        return {"message": "No genre"}

    query = update(Genre).filter_by(id=genre_id).values(name=new_name)
    await db.execute(query)
    await db.commit()

    updated_genre = await db.execute(select(Genre).filter_by(id=genre_id))
    updated_genre = updated_genre.scalar()
    return updated_genre
