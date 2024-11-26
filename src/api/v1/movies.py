from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.base import MovieDAO
from src.db.database import get_db
from src.models.movies import MovieReadSchema, MoviePutSchema

router = APIRouter()


@router.get("/{movie_id}")
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)) -> MovieReadSchema:
    movie = await MovieDAO.get_detail_joined(movie_id, db)
    return MovieReadSchema.model_validate(movie, from_attributes=True)


@router.get("/")
async def get_movie(db: AsyncSession = Depends(get_db)) -> list[MovieReadSchema]:
    movies = await MovieDAO.get_all_joined_movies(db)
    return [MovieReadSchema.model_validate(movie, from_attributes=True) for movie in movies]


@router.put("/{movie_id}")
async def update_movie(movie_id: int, new_data: MoviePutSchema,
                       db: AsyncSession = Depends(get_db)) -> MoviePutSchema:
    updated_movie = MovieDAO.update(movie_id, new_data, db)
    return MoviePutSchema.model_validate(updated_movie, from_attributes=True)


@router.delete("/{movie_id}")
async def delete_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await MovieDAO.delete(movie_id, db)
    return {"Message": f"Movie deleted {result}, id {movie_id}"}
