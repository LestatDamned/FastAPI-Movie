from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from parser.parser import bulk_films, get_api_movie
from parser.utils import get_movie_to_schema, save_movie_to_db
from src.db.database import get_db
from src.models.models import LoadMovieFromAPI
from src.models.movies import MovieCreateSchema

router = APIRouter()


@router.post("/eat_movies/")
async def eat_movies(db: AsyncSession = Depends(get_db)):
    movies_list = await bulk_films()

    json_list = [await get_api_movie(LoadMovieFromAPI.model_validate(movie)) for movie in movies_list]

    movie_data = [get_movie_to_schema(movie) for movie in json_list]

    movies_data = [await save_movie_to_db(movie, db) for movie in movie_data]
    return movies_data


@router.post("/save_movie_to_db/")
async def save_movie_to_database(movie: LoadMovieFromAPI, db: AsyncSession = Depends(get_db)):
    result = await get_api_movie(movie)
    movie_data = get_movie_to_schema(result)
    saved_movie = await save_movie_to_db(movie_data, db)
    return saved_movie


@router.get("/fetch_movie/")
async def fetch_movie(movie: LoadMovieFromAPI) -> MovieCreateSchema:
    result = await get_api_movie(movie)
    movie = get_movie_to_schema(result)
    return movie
