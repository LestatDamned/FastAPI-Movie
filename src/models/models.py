from pydantic import BaseModel

from src.db.tables import Language


class GenreSchema(BaseModel):
    name: str


class DirectorSchema(BaseModel):
    name: str


class WriterSchema(BaseModel):
    name: str


class ActorSchema(BaseModel):
    name: str


class CountrySchema(BaseModel):
    name: str


class RatingSchema(BaseModel):
    source: str
    value: str


class LanguageSchema(BaseModel):
    name: str


class MovieSchema(BaseModel):
    Title: str
    Year: int
    Released: str
    Runtime: str
    Genre: list[GenreSchema]
    Director: list[DirectorSchema]
    Writer: list[WriterSchema]
    Actors: list[ActorSchema]
    Plot: str
    Language: list[LanguageSchema]
    Country: list[CountrySchema]
    Awards: str
    Poster: str
    Ratings: list[RatingSchema]
    Metascore: str
    imdbRating: str
    imdbID: str
    BoxOffice: str
