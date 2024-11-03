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
from src.db.tables import Movie, Director, Actor, Genre, Writer, Country, Rating, Language

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


@router.get("/directors/")
async def get_director(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Director))
    director = result.scalars().all()
    return director


@router.get("/directors/{director_id}")
async def get_director(director_id: int, db: AsyncSession = Depends(get_db)):
    query = (select(Director).filter_by(id=director_id))
    db_movie = await db.execute(query)
    db_movie = db_movie.scalar()
    return db_movie


@router.patch("/directors/{director_id}")
async def update_director(director_id: int, new_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Director).filter_by(id=director_id))
    movie = result.scalar_one_or_none()
    if movie is None:
        return {"Message": "Director not found."}
    query = update(Director).filter_by(id=director_id).values(name=new_name)
    await db.execute(query)
    await db.commit()

    updated_movie = await db.execute(select(Director).filter_by(id=director_id))
    updated_movie = updated_movie.scalar()
    return updated_movie


@router.get("/actors/")
async def get_actor(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Actor))
    actors = result.scalars().all()
    return actors


@router.get("/actors/{actor_id}/")
async def get_actor(actor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Actor).filter_by(id=actor_id))
    actors = result.scalar_one_or_none()
    if actors is None:
        return {"message": "No actors"}
    return actors


@router.patch("/actors/{actor_id}/")
async def update_actor(actor_id: int, new_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Actor).filter_by(id=actor_id))
    actor = result.scalar_one_or_none()
    if actor is None:
        return {"message": "No actors"}

    query = update(Actor).filter_by(id=actor_id).values(name=new_name)
    await db.execute(query)
    await db.commit()

    updated_actor = await db.execute(select(Actor).filter_by(id=actor_id))
    updated_actor = updated_actor.scalar()
    return updated_actor


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


@router.get("/writers/")
async def get_writer(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Writer))
    writers = result.scalars().all()
    return writers


@router.get("/writers/{writer_id}/")
async def get_writer(writer_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Writer).filter_by(id=writer_id))
    writers = result.scalar_one_or_none()
    if writers is None:
        return {"message": "No writers"}
    return writers


@router.patch("/writers/{writer_id}/")
async def update_writer(writer_id: int, new_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Writer).filter_by(id=writer_id))
    writer = result.scalar_one_or_none()
    if writer is None:
        return {"message": "No writers"}

    query = update(Writer).filter_by(id=writer_id).values(name=new_name)
    await db.execute(query)
    await db.commit()

    updated_writer = await db.execute(select(Writer).filter_by(id=writer_id))
    updated_writer = updated_writer.scalar()
    return updated_writer


@router.get("/countries/")
async def get_country(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country))
    countries = result.scalars().all()
    return countries


@router.get("/countries/{country_id}/")
async def get_country(country_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country).filter_by(id=country_id))
    countries = result.scalar_one_or_none()
    if countries is None:
        return {"message": "No countries"}
    return countries


@router.patch("/countries/{country_id}/")
async def update_country(country_id: int, new_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country).filter_by(id=country_id))
    country = result.scalar_one_or_none()
    if country is None:
        return {"message": "No countries"}

    await db.execute(update(Country).filter_by(id=country_id).values(name=new_name))
    await db.commit()

    updated_country = await db.execute(select(Country).filter_by(id=country_id))
    updated_country = updated_country.scalar()
    return updated_country


@router.get("/ratings/")
async def get_rating(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Rating))
    ratings = result.scalars().all()
    return ratings


@router.get("/ratings/{rating_id}/")
async def get_rating(rating_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Rating).filter_by(id=rating_id))
    rating = result.scalar_one_or_none()
    if rating is None:
        return {"message": "No ratings"}
    return rating


@router.patch("/ratings/{rating_id}/")
async def update_rating(rating_id: int, new_source: str, new_value: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Rating).filter_by(id=rating_id))
    rating = result.scalar_one_or_none()
    if rating is None:
        return {"message": "No ratings"}

    await db.execute(update(Rating).filter_by(id=rating_id).values(source=new_source, value=new_value))
    await db.commit()

    updated_rating = await db.execute(select(Rating).filter_by(id=rating_id))
    updated_rating = updated_rating.scalar()
    return updated_rating


@router.get("/languages/")
async def get_languages(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Language))
    languages = result.scalars().all()
    return languages


@router.get("/languages/{language_id}/")
async def get_language(language_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Language).filter_by(id=language_id))
    language = result.scalar_one_or_none()
    if language is None:
        return {"message": "No languages"}


@router.patch("/languages/{language_id}/")
async def update_language(language_id: int, new_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Language).filter_by(id=(language_id,)))
    language = result.scalar_one_or_none()
    if language is None:
        return {"message": "No languages"}

    await db.execute(update(Language).filter_by(id=language_id).values(name=new_name))
    await db.commit()

    updated_language = await db.execute(select(Language).filter_by(id=language_id))
    updated_language = updated_language.scalar()
    return updated_language
