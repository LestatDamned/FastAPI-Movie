from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from src.db.database import get_db
from src.db.tables import Movie, Actor, Country, Director, Genre, Language, Rating


class BaseDAO:
    model = None

    @classmethod
    async def get_all(cls, db: AsyncSession = Depends(get_db)):
        query = select(cls.model)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_all_joined(cls, db: AsyncSession = Depends(get_db), **joined):
        query = select(cls.model)
        for relation, enabled in joined.items():
            if enabled:
                query = query.options(joinedload(getattr(cls.model, relation)))
        result = await db.execute(query)
        return result.unique().scalars().all()

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
    async def get_joined_movies(cls, db: AsyncSession = Depends(get_db)):
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
        search_actor_name = search_actor_name.scalar_one_or_none()
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


class RBJoinedMovie:
    def __init__(self,
                 actors: bool | None = None,
                 director: bool | None = None,
                 language: bool | None = None,
                 genres: bool | None = None,
                 writer: bool | None = None,
                 country: bool | None = None,
                 ratings: bool | None = None, ):
        self.actors = actors
        self.director = director
        self.language = language
        self.genres = genres
        self.writer = writer
        self.country = country
        self.ratings = ratings

    def to_dict(self) -> dict:
        data = {"actors": self.actors, "director": self.director, "language": self.language, "genres": self.genres,
                "writer": self.writer, "country": self.country, "ratings": self.ratings}

        filtered_data = {key: value for key, value in data.items() if value}

        return filtered_data


class RBFilters:
    def __init__(self,
                 actor: int | None = None,
                 director: int | None = None,
                 language: int | None = None,
                 genres: int | None = None,
                 writer: int | None = None,
                 country: int | None = None,
                 ratings: int | None = None):
        self.actor = actor
        self.director = director
        self.language = language
        self.genres = genres
        self.writer = writer
        self.country = country
        self.ratings = ratings

    def to_dict(self) -> dict:
        data = {"actor": self.actor, "director": self.director, "language": self.language,
                "genres": self.genres, "writer": self.writer, "country": self.country, "ratings": self.ratings}

        filtered_data = {key: value for key, value in data.items() if value}

        return filtered_data
