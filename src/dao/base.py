from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from src.db.database import get_db
from src.db.tables import Movie, Actor, Country, Director, Genre, Language, Rating, Writer


class BaseDAO:
    model = None

    @classmethod
    async def get_all(cls, db: AsyncSession = Depends(get_db)):
        query = select(cls.model)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, instance_id: int, db: AsyncSession = Depends(get_db)):
        query = select(cls.model).filter_by(id=instance_id)
        result = await db.execute(query)
        result = result.scalar_one_or_none()
        if result is None:
            raise HTTPException(status_code=404, detail="Object not found")
        return result

    @classmethod
    async def update(cls, instance_id: int, new_values: type(BaseModel), db: AsyncSession = Depends(get_db)):
        query = select(cls.model).filter_by(id=instance_id)
        result = await db.execute(query)
        if result.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail="Not Found")

        update_data = update(cls.model).filter_by(id=instance_id).values(**new_values.model_dump(exclude_unset=True))
        await db.execute(update_data)
        await db.commit()

        update_query = select(cls.model).filter_by(id=instance_id)
        result = await db.execute(update_query)
        return result.scalar()

    @classmethod
    async def get_with_movies(cls, name: str, db: AsyncSession = Depends(get_db)):
        query = select(cls.model).options(joinedload(cls.model.movies)).filter(cls.model.name.ilike(f"%{name}%"))
        result = await db.execute(query)
        return result.unique().scalars().all()

    @classmethod
    async def delete(cls, instance_id: int, db: AsyncSession = Depends(get_db)):
        query = delete(cls.model).filter_by(id=instance_id)
        result = await db.execute(query)
        try:
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
        return result.rowcount


class MovieDAO(BaseDAO):
    model = Movie

    @classmethod
    async def get_detail_joined(cls, movie_id: int, db: AsyncSession = Depends(get_db)):
        query = (select(cls.model).filter_by(id=movie_id)
                 .options(joinedload(cls.model.director),
                          joinedload(cls.model.actors),
                          joinedload(cls.model.language),
                          joinedload(cls.model.genres),
                          joinedload(cls.model.writer),
                          joinedload(cls.model.country),
                          joinedload(cls.model.ratings)))
        movie = await db.execute(query)
        movie = movie.unique().scalar_one_or_none()
        if movie is None:
            raise HTTPException(status_code=404, detail="Movie not found")
        return movie

    @classmethod
    async def get_all_joined_movies(cls, db: AsyncSession = Depends(get_db)):
        query = (select(cls.model).options(joinedload(cls.model.director),
                                           joinedload(cls.model.actors),
                                           joinedload(cls.model.language),
                                           joinedload(cls.model.genres),
                                           joinedload(cls.model.writer),
                                           joinedload(cls.model.country),
                                           joinedload(cls.model.ratings)))
        movie = await db.execute(query)
        if movie.unique().scalars() is None:
            raise HTTPException(status_code=404, detail="Movie not found")
        return movie.unique().scalars()


class ActorDAO(BaseDAO):
    model = Actor

    @classmethod
    async def get_movie_with_actor(cls, actor_name: str, db: AsyncSession = Depends(get_db)):
        search_actor_name = await db.execute(select(cls.model).filter(cls.model.name.ilike(f"%{actor_name}%")))
        search_actor_name = search_actor_name.scalars().first()
        if search_actor_name is None:
            raise HTTPException(status_code=404, detail="Actor not found")
        query = (select(Movie).join(Movie.actors).filter_by(id=search_actor_name.id)
                 .options(joinedload(Movie.actors),
                          joinedload(Movie.director),
                          joinedload(Movie.language),
                          joinedload(Movie.genres),
                          joinedload(Movie.writer),
                          joinedload(Movie.country),
                          joinedload(Movie.ratings)))
        result = await db.execute(query)
        movies = result.unique().scalars().all()
        return movies

    @classmethod
    async def get_by_name(cls, actor_name: str, db: AsyncSession = Depends(get_db)):
        query = (select(Movie).options(joinedload(Movie.actors),
                                       joinedload(Movie.director),
                                       joinedload(Movie.language),
                                       joinedload(Movie.genres),
                                       joinedload(Movie.writer),
                                       joinedload(Movie.country),
                                       joinedload(Movie.ratings)).
                 filter(Movie.actors.any(Actor.name.ilike(f"%{actor_name}%"))))
        result = await db.execute(query)
        movie = result.unique().scalars()
        print(movie)
        if not movie:
            raise HTTPException(status_code=404, detail="Actor not found")
        return movie


class CountriesDAO(BaseDAO):
    model = Country


class DirectorsDAO(BaseDAO):
    model = Director


class GenresDAO(BaseDAO):
    model = Genre


class LanguagesDAO(BaseDAO):
    model = Language


class RatingsDAO(BaseDAO):
    model = Rating


class WritersDAO(BaseDAO):
    model = Writer
