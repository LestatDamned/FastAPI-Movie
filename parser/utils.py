from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from parser.parser import get_detail_actor_from_api
from src.db.tables import Movie, Genre, Director, Writer, Country, Rating, Language, Actor, Base
from src.models.models import GenreSchema, DirectorSchema, WriterSchema, ActorSchema, CountrySchema, \
    RatingSchema, LanguageSchema, MovieSchemaWrite, ActorDetailSchema


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


async def save_movie_to_db(movie_data: MovieSchemaWrite, db: AsyncSession):
    movie = Movie(
        title=movie_data.Title,
        year=movie_data.Year,
        release_date=movie_data.Released,
        runtime=movie_data.Runtime,
        plot=movie_data.Plot,
        awards=movie_data.Awards,
        poster=movie_data.Poster,
        metascore=movie_data.Metascore,
        imdb_rating=movie_data.imdbRating,
        imdb_id=movie_data.imdbID,
        box_office=movie_data.BoxOffice,
    )

    genres = await populate_fields(db, movie_data.Genre, Genre)
    directors = await populate_fields(db, movie_data.Director, Director)
    writers = await populate_fields(db, movie_data.Writer, Writer)
    countries = await populate_fields(db, movie_data.Country, Country)
    languages = await populate_fields(db, movie_data.Language, Language)
    ratings = [Rating(source=rating.source, value=rating.value) for rating in movie_data.Ratings]

    actors_list = []
    for actor in movie_data.Actors:
        existing_actor = await db.execute(select(Actor).filter_by(name=actor.name))
        existing_actor = existing_actor.scalar_one_or_none()
        if existing_actor is None:
            new_actor = await get_detail_actor_from_api(actor.name)
            new_actor = ActorDetailSchema.model_validate(new_actor, from_attributes=True)
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


def get_movie_to_schema(result: dict) -> MovieSchemaWrite:
    genres = [GenreSchema(name=genre.strip()) for genre in result["Genre"].split(",")]
    directors = [DirectorSchema(name=director.strip()) for director in result["Director"].split(",")]
    writers = [WriterSchema(name=writer.strip()) for writer in result["Writer"].split(",")]
    actors = [ActorSchema(name=actor.strip()) for actor in result["Actors"].split(",")]
    country = [CountrySchema(name=country.strip()) for country in result["Country"].split(",")]
    rating = [RatingSchema(source=rating["Source"], value=rating["Value"]) for rating in result.get("Ratings", [])]
    language = [LanguageSchema(name=language.strip()) for language in result["Language"].split(",")]

    movie = MovieSchemaWrite(
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
