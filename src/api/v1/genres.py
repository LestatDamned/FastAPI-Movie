from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.tables import Genre
from src.models.models import GenreSchema

router = APIRouter()


@router.get("/genres/")
async def get_genre(db: AsyncSession = Depends(get_db)) -> list[GenreSchema]:
    result = await db.execute(select(Genre))
    genres = result.scalars().all()
    return [GenreSchema.model_validate(genre, from_attributes=True) for genre in genres]


@router.get("/genres/{genre_id}/")
async def get_genre(genre_id: int, db: AsyncSession = Depends(get_db)) -> GenreSchema:
    result = await db.execute(select(Genre).filter_by(id=genre_id))
    genres = result.scalar_one_or_none()
    if genres is None:
        HTTPException(status_code=404, detail="Genre not found")
    return GenreSchema.model_validate(genres, from_attributes=True)


@router.patch("/genres/{genre_id}/")
async def update_genre(genre_id: int, new_name: str, db: AsyncSession = Depends(get_db)) -> GenreSchema:
    result = await db.execute(select(Genre).filter_by(id=genre_id))
    genre = result.scalar_one_or_none()
    if genre is None:
        HTTPException(status_code=404, detail="Genre not found")

    query = update(Genre).filter_by(id=genre_id).values(name=new_name)
    await db.execute(query)
    await db.commit()

    updated_genre = await db.execute(select(Genre).filter_by(id=genre_id))
    updated_genre = updated_genre.scalar()
    return GenreSchema.model_validate(updated_genre, from_attributes=True)
