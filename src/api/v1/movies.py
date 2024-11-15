from select import select

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from parser.parser import get_api_movie, bulk_films
from parser.utils import get_movie_to_schema, save_movie_to_db
from src.db.database import get_db
from src.db.tables import Movie
from src.models.models import MovieCreateSchema, MovieReadSchema, MoviePutSchema

router = APIRouter()


@router.get("/eat_movies/")
async def eat_movies(db: AsyncSession = Depends(get_db)):
    movies_list = await bulk_films()

    json_list = [await get_api_movie(movie, 2023) for movie in movies_list]

    movie_data = [get_movie_to_schema(movie) for movie in json_list]

    movies_data = [await save_movie_to_db(movie, db) for movie in movie_data]
    return movies_data


@router.get("/save_movie_to_db/")
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


@router.get("/movie/{movie_id}")
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    query = (select(Movie).filter_by(id=movie_id).options(
        joinedload(Movie.actors),
        joinedload(Movie.director),
        joinedload(Movie.language),
        joinedload(Movie.genres),
        joinedload(Movie.writer),
        joinedload(Movie.country),
        joinedload(Movie.ratings)))
    result = await db.execute(query)
    movie = result.unique().scalar_one_or_none()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return MovieReadSchema.model_validate(movie, from_attributes=True)


@router.get("/movies/")
async def get_movie(db: AsyncSession = Depends(get_db)):
    query = (select(Movie).options(
        joinedload(Movie.actors),
        joinedload(Movie.director),
        joinedload(Movie.language),
        joinedload(Movie.genres),
        joinedload(Movie.writer),
        joinedload(Movie.country),
        joinedload(Movie.ratings)))
    result = await db.execute(query)
    movies = result.unique().scalars().all()
    return [MovieReadSchema.model_validate(movie, from_attributes=True) for movie in movies]


@router.put("/movie/{movie_id}")
async def update_movie(movie_id: int, new_data: MoviePutSchema,
                       db: AsyncSession = Depends(get_db)) -> MoviePutSchema:
    result = await db.execute(select(Movie).filter_by(id=movie_id))
    movie = result.scalar_one_or_none()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    query = update(Movie).filter_by(id=movie_id).values(**new_data.model_dump(exclude_unset=True))
    await db.execute(query)
    await db.commit()

    updated_movie = await db.execute(select(Movie).filter_by(id=movie_id))
    updated_movie = updated_movie.scalar()
    return MoviePutSchema.model_validate(updated_movie, from_attributes=True)


@router.delete("/movie/{movie_id}")
async def delete_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie).filter_by(id=movie_id))
    movie = result.scalar_one_or_none()
    if movie is None:
        return {"Message": "Movie not found."}
    query = delete(Movie).filter_by(id=movie_id)
    del_result = await db.execute(query)
    await db.commit()
    return {"Message": f"Movie deleted {del_result.rowcount}, id {movie_id}"}
