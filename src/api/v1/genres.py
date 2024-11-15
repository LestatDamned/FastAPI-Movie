from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.tables import Genre
from src.models.models import GenreReadSchema, GenreCreateSchema

router = APIRouter()


@router.get("/genres/")
async def get_genre(db: AsyncSession = Depends(get_db)) -> list[GenreReadSchema]:
    result = await db.execute(select(Genre))
    genres = result.scalars().all()
    return [GenreReadSchema.model_validate(genre, from_attributes=True) for genre in genres]


@router.get("/genres/{genre_id}/")
async def get_genre(genre_id: int, db: AsyncSession = Depends(get_db)) -> GenreReadSchema:
    result = await db.execute(select(Genre).filter_by(id=genre_id))
    genres = result.scalar_one_or_none()
    if genres is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return GenreReadSchema.model_validate(genres, from_attributes=True)


@router.patch("/genres/{genre_id}/")
async def update_genre(genre_id: int, new_data: GenreCreateSchema,
                       db: AsyncSession = Depends(get_db)) -> GenreReadSchema:
    result = await db.execute(select(Genre).filter_by(id=genre_id))
    genre = result.scalar_one_or_none()
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")

    query = update(Genre).filter_by(id=genre_id).values(**new_data.model_dump(exclude_unset=True))
    await db.execute(query)
    await db.commit()

    updated_genre = await db.execute(select(Genre).filter_by(id=genre_id))
    updated_genre = updated_genre.scalar()
    return GenreReadSchema.model_validate(updated_genre, from_attributes=True)
