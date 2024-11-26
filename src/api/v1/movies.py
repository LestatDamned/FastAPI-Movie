from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from parser.parser import get_api_movie, bulk_films
from parser.utils import get_movie_to_schema, save_movie_to_db
from src.dao.base import MovieDAO
from src.db.database import get_db
from src.db.tables import Movie
from src.models.movies import MovieCreateSchema, MovieReadSchema, MoviePutSchema

router = APIRouter()


@router.post("/eat_movies/")
async def eat_movies(db: AsyncSession = Depends(get_db)):
    movies_list = await bulk_films()

    json_list = [await get_api_movie(movie, 2023) for movie in movies_list]

    movie_data = [get_movie_to_schema(movie) for movie in json_list]

    movies_data = [await save_movie_to_db(movie, db) for movie in movie_data]
    return movies_data


@router.post("/save_movie_to_db/")
async def save_movie_to_database(movie: str, year: int, db: AsyncSession = Depends(get_db)):
    result = await get_api_movie(movie, year)
    movie_data = get_movie_to_schema(result)
    saved_movie = await save_movie_to_db(movie_data, db)
    return saved_movie


@router.get("/fetch_movie/")
async def fetch_movie(movie: str, year: int) -> MovieCreateSchema:
    result = await get_api_movie(movie, year)
    movie = get_movie_to_schema(result)
    return movie


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
