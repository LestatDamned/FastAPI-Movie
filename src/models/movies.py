from pydantic import BaseModel, Field

from src.models.actors import ActorSchema
from src.models.countries import CountryReadSchema
from src.models.directors import DirectorReadSchema
from src.models.genres import GenreReadSchema
from src.models.languages import LanguageReadSchema
from src.models.ratings import RatingReadSchema
from src.models.writers import WriterReadSchema


class MovieCreateSchema(BaseModel):
    title: str = Field(alias="Title")
    year: int = Field(alias="Year")
    release_date: str = Field(alias="Released")
    runtime: str = Field(alias="Runtime")
    genre: list[GenreReadSchema] = Field(alias="Genre")
    director: list[DirectorReadSchema] = Field(alias="Director")
    writer: list[WriterReadSchema] = Field(alias="Writer")
    actors: list[ActorSchema] = Field(alias="Actors")
    plot: str = Field(alias="Plot")
    language: list[LanguageReadSchema] = Field(alias="Language")
    country: list[CountryReadSchema] = Field(alias="Country")
    awards: str = Field(alias="Awards")
    poster: str = Field(alias="Poster")
    ratings: list[RatingReadSchema] = Field(alias="Ratings")
    metascore: str = Field(alias="Metascore")
    imdb_rating: str = Field(alias="imdbRating")
    imdb_id: str = Field(alias="imdbID")
    box_office: str = Field(alias="BoxOffice")


class MovieReadSchema(BaseModel):
    id: int
    title: str
    year: int
    release_date: str
    runtime: str
    genres: list[GenreReadSchema]
    director: list[DirectorReadSchema]
    writer: list[WriterReadSchema]
    actors: list[ActorSchema]
    plot: str
    language: list[LanguageReadSchema]
    country: list[CountryReadSchema]
    awards: str
    poster: str
    ratings: list[RatingReadSchema]
    metascore: str
    imdb_rating: str
    imdb_id: str
    box_office: str


class MoviePutSchema(BaseModel):
    title: str
    year: int
    release_date: str
    runtime: str
    plot: str
    awards: str
    poster: str
    metascore: str
    imdb_rating: str
    imdb_id: str
    box_office: str
