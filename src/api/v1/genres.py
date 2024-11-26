from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.base import GenresDAO
from src.db.database import get_db
from src.models.genres import GenreCreateSchema, GenreReadSchema

router = APIRouter()


@router.get("/")
async def get_genre(db: AsyncSession = Depends(get_db)) -> list[GenreReadSchema]:
    genres = await GenresDAO.get_all(db)
    return [GenreReadSchema.model_validate(genre, from_attributes=True) for genre in genres]


@router.get("/{genre_id}/")
async def get_genre(genre_id: int, db: AsyncSession = Depends(get_db)) -> GenreReadSchema:
    genres = await GenresDAO.get_by_id(genre_id, db)
    return GenreReadSchema.model_validate(genres, from_attributes=True)


@router.patch("/{genre_id}/")
async def update_genre(genre_id: int, new_data: GenreCreateSchema,
                       db: AsyncSession = Depends(get_db)) -> GenreReadSchema:
    updated_genre = GenresDAO.update(genre_id, new_data, db)
    return GenreReadSchema.model_validate(updated_genre, from_attributes=True)


@router.get("/movies/{name}")
async def get_by_name(name: str, db: AsyncSession = Depends(get_db)):
    genres = GenresDAO.get_with_movies(name, db)
    return genres
