from typing import List

from fastapi import APIRouter

from app.schemans import MovieSchema, GenreSchema, DirectorSchema, ActorSchema, WriterSchema, CountrySchema, \
    RatingSchema
from parser.parser import get_api_movie

router = APIRouter()


@router.get("/fetch_movie/")
async def fetch_movie(movie: str, year: int):

    result = await get_api_movie(movie, year)
    genres = [GenreSchema(name=genre.strip()) for genre in result["Genre"].split(",")]
    directors = [DirectorSchema(name=director.strip()) for director in result["Director"].split(",")]
    writers = [WriterSchema(name=writer.strip()) for writer in result["Writer"].split(",")]
    actors = [ActorSchema(name=actor.strip()) for actor in result["Actors"].split(",")]
    country = [CountrySchema(name=country.strip()) for country in result["Country"].split(",")]
    rating = [RatingSchema(source=rating["Source"], value=rating["Value"]) for rating in result.get("Ratings", [])]

    res = MovieSchema(
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
    print(res)
    return result


@router.get("/movie/{movie_id}")
async def get_movie(movie_id: int):
    return movie_id


@router.get("/movie/")
async def get_movie(movie: List[MovieSchema]):
    return movie


@router.post("/movie/")
async def create_movie(movie: MovieSchema):
    return movie


@router.put("/movie/{movie_id}")
async def update_movie(movie_id: int, movie: MovieSchema):
    return movie


@router.delete("/movie/{movie_id}")
async def delete_movie(movie_id: int):
    return movie_id
