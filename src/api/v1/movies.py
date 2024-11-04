from select import select

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from parser.parser import get_api_movie
from parser.utils import get_movie_to_schema, save_movie_to_db
from src.db.database import get_db
from src.db.tables import Movie

router = APIRouter()


@router.get("/save_movie_to_db/")
async def save_movie_to_database(movie: str, year: int, db: AsyncSession = Depends(get_db)):
    result = await get_api_movie(movie, year)
    movie_data = get_movie_to_schema(result)
    saved_movie = await save_movie_to_db(movie_data, db)
    return saved_movie


@router.get("/fetch_movie/")
async def fetch_movie(movie: str, year: int):
    result = await get_api_movie(movie, year)
    movie = get_movie_to_schema(result)
    return movie


@router.get("/movie/{movie_id}/detail/")
async def get_movie_detail(movie_id: int, db: AsyncSession = Depends(get_db)):
    query = (select(Movie).options(
        joinedload(Movie.actors),
        joinedload(Movie.director),
        joinedload(Movie.language),
        joinedload(Movie.genres),
        joinedload(Movie.writer),
        joinedload(Movie.country),
        joinedload(Movie.ratings)).filter_by(id=movie_id))
    db_movie = await db.execute(query)
    db_movie = db_movie.scalar()
    return db_movie


@router.get("/movie/{movie_id}")
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    query = (select(Movie).filter_by(id=movie_id))
    db_movie = await db.execute(query)
    db_movie = db_movie.scalar()
    return db_movie


@router.get("/movies/")
async def get_movie(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie))
    movies = result.scalars().all()
    return movies


@router.patch("/movie/{movie_id}")
async def update_movie(movie_id: int, new_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie).filter_by(id=movie_id))
    movie = result.scalar_one_or_none()
    if movie is None:
        return {"Message": "Movie not found."}
    query = update(Movie).filter_by(id=movie_id).values(title=new_name)
    await db.execute(query)
    await db.commit()

    updated_movie = await db.execute(select(Movie).filter_by(id=movie_id))
    updated_movie = updated_movie.scalar()
    return updated_movie


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
