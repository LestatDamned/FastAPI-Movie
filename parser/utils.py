from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from parser.parser import get_detail_actor_from_api
from src.db.tables import Movie, Genre, Director, Writer, Country, Rating, Language, Actor, Base
from src.models.models import GenreReadSchema, DirectorReadSchema, WriterReadSchema, ActorSchema, CountryReadSchema, \
    RatingReadSchema, LanguageReadSchema, ActorCreateSchema, MovieCreateSchema


async def populate_fields(db: AsyncSession, movie_data: list[BaseModel], db_instance: type[Base]):
    data_list = []
    for data in movie_data:
        existing_data = await db.execute(select(db_instance).filter_by(name=data.name))
        existing_data = existing_data.scalar_one_or_none()
        if existing_data is None:
            new_data = db_instance(name=data.name)
            db.add(new_data)
            await db.commit()
            data_list.append(new_data)
        else:
            data_list.append(existing_data)
    return data_list


async def save_movie_to_db(movie_data: MovieCreateSchema, db: AsyncSession):
    movie = Movie(
        title=movie_data.title,
        year=movie_data.year,
        release_date=movie_data.release_date,
        runtime=movie_data.runtime,
        plot=movie_data.plot,
        awards=movie_data.awards,
        poster=movie_data.poster,
        metascore=movie_data.metascore,
        imdb_rating=movie_data.imdb_rating,
        imdb_id=movie_data.imdb_id,
        box_office=movie_data.box_office,
    )

    genres = await populate_fields(db, movie_data.genre, Genre)
    directors = await populate_fields(db, movie_data.director, Director)
    writers = await populate_fields(db, movie_data.writer, Writer)
    countries = await populate_fields(db, movie_data.country, Country)
    languages = await populate_fields(db, movie_data.language, Language)
    ratings = [Rating(source=rating.source, value=rating.value) for rating in movie_data.ratings]

    actors_list = []
    for actor in movie_data.actors:
        existing_actor = await db.execute(select(Actor).filter_by(name=actor.name))
        existing_actor = existing_actor.scalar_one_or_none()
        if existing_actor is None:
            new_actor = await get_detail_actor_from_api(actor.name)
            new_actor = ActorCreateSchema.model_validate(new_actor, from_attributes=True)
            new_actor = new_actor.model_dump()
            actors_list.append(Actor(**new_actor))
        else:
            actors_list.append(existing_actor)

    movie.genres = genres
    movie.director = directors
    movie.writer = writers
    movie.actors = actors_list
    movie.country = countries
    movie.ratings = ratings
    movie.language = languages
    db.add(movie)
    await db.commit()
    await db.refresh(movie)
    return movie


def get_movie_to_schema(result: dict) -> MovieCreateSchema:
    genres = [GenreReadSchema(name=genre.strip()) for genre in result["Genre"].split(",")]
    directors = [DirectorReadSchema(name=director.strip()) for director in result["Director"].split(",")]
    writers = [WriterReadSchema(name=writer.strip()) for writer in result["Writer"].split(",")]
    actors = [ActorSchema(name=actor.strip()) for actor in result["Actors"].split(",")]
    country = [CountryReadSchema(name=country.strip()) for country in result["Country"].split(",")]
    rating = [RatingReadSchema(source=rating["Source"], value=rating["Value"]) for rating in result.get("Ratings", [])]
    language = [LanguageReadSchema(name=language.strip()) for language in result["Language"].split(",")]

    movie = MovieCreateSchema(
        Title=result["Title"],
        Year=result["Year"],
        Released=result["Released"],
        Runtime=result["Runtime"],
        Genre=genres,
        Director=directors,
        Writer=writers,
        Actors=actors,
        Plot=result["Plot"],
        Language=language,
        Country=country,
        Awards=result["Awards"],
        Poster=result["Poster"],
        Ratings=rating,
        Metascore=result["Metascore"],
        imdbRating=result["imdbRating"],
        imdbID=result["imdbID"],
        BoxOffice=result["BoxOffice"],
    )
    return movie
