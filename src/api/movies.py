from select import select

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from parser.parser import get_api_movie
from parser.utils import get_movie_to_schema, save_movie_to_db
from src.db.database import get_db
from src.db.tables import Movie, Director, Actor, Genre, Writer, Country, Rating, Language
from src.models.models import MovieSchema

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


@router.get("/movie/{movie_id}")
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    db_movie = await db.execute(select(Movie).where(Movie.id == movie_id))
    return db_movie


@router.get("/movies/")
async def get_movie(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie))
    movies = result.scalars().all()
    return movies


@router.get("/directors/")
async def get_movie(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Director))
    director = result.scalars().all()
    return director


@router.get("/actors/")
async def get_movie(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Actor))
    actors = result.scalars().all()
    return actors


@router.get("/actors/{actor_id}/")
async def get_movie(actor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Actor).filter(Actor.id == actor_id))
    actors = result.scalar_one_or_none()
    if actors is None:
        return {"message": "No actors"}
    return actors


@router.get("/genres/")
async def get_movie(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Genre))
    genres = result.scalars().all()
    return genres


@router.get("/writers/")
async def get_movie(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Writer))
    writers = result.scalars().all()
    return writers


@router.get("/countries/")
async def get_movie(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country))
    countries = result.scalars().all()
    return countries


@router.get("/ratings/")
async def get_movie(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Rating))
    ratings = result.scalars().all()
    return ratings


@router.get("/languages/")
async def get_movie(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Language))
    languages = result.scalars().all()
    return languages


@router.post("/movie/")
async def create_movie(movie: MovieSchema):
    return movie


@router.put("/movie/{movie_id}")
async def update_movie(movie_id: int, movie: MovieSchema):
    return movie


@router.delete("/movie/{movie_id}")
async def delete_movie(movie_id: int):
    return movie_id
