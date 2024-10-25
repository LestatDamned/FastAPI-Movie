from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Movie, Genre, Director, Writer, Actor, Country, Rating
from app.schemans import MovieSchema, GenreSchema, DirectorSchema, WriterSchema, ActorSchema, CountrySchema, \
    RatingSchema


async def save_movie_to_db(movie_data: MovieSchema, db: AsyncSession):
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
    genres = [Genre(name=genre.name) for genre in movie_data.Genre]
    director = [Director(name=director.name) for director in movie_data.Director]
    writer = [Writer(name=writer.name) for writer in movie_data.Writer]
    actor = [Actor(name=actor.name) for actor in movie_data.Actors]
    country = [Country(name=country.name) for country in movie_data.Country]
    rating = [Rating(source=rating.source, value=rating.value) for rating in movie_data.Ratings]

    movie.genres.extend(genres)
    movie.director.extend(director)
    movie.writer.extend(writer)
    movie.actors.extend(actor)
    movie.country.extend(country)
    movie.ratings.extend(rating)

    db.add(movie)
    await db.commit()
    await db.refresh(movie)
    return movie


def get_movie_to_schema(result: dict) -> MovieSchema:
    genres = [GenreSchema(name=genre.strip()) for genre in result["Genre"].split(",")]
    directors = [DirectorSchema(name=director.strip()) for director in result["Director"].split(",")]
    writers = [WriterSchema(name=writer.strip()) for writer in result["Writer"].split(",")]
    actors = [ActorSchema(name=actor.strip()) for actor in result["Actors"].split(",")]
    country = [CountrySchema(name=country.strip()) for country in result["Country"].split(",")]
    rating = [RatingSchema(source=rating["Source"], value=rating["Value"]) for rating in result.get("Ratings", [])]

    movie = MovieSchema(
        Title=result["Title"],
        Year=result["Year"],
        Released=result["Released"],
        Runtime=result["Runtime"],
        Genre=genres,
        Director=directors,
        Writer=writers,
        Actors=actors,
        Plot=result["Plot"],
        Language=result["Language"],
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
