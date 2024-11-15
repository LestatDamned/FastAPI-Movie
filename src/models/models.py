from datetime import date

from pydantic import BaseModel, Field, field_validator


class GenreCreateSchema(BaseModel):
    name: str


class GenreReadSchema(BaseModel):
    id: int
    name: str


class DirectorReadSchema(BaseModel):
    id: int
    name: str


class DirectorCreateSchema(BaseModel):
    name: str


class WriterReadSchema(BaseModel):
    id: int
    name: str


class WriterCreateSchema(BaseModel):
    name: str


class ActorSchema(BaseModel):
    name: str


class ActorCreateSchema(ActorSchema):
    bio: str | None = Field(alias="biography")
    place_of_birth: str | None = Field()
    gender: str | None = Field(description="Gender send 1 for Woman, send 2 for Man")
    birthdate: date | None = Field(alias="birthday")
    homepage: str | None = Field(alias="homepage")

    @field_validator("gender", mode="before")
    def convert_gender(cls, value):
        if value == 1:
            return "Woman"
        elif value == 2:
            return "Male"
        else:
            return "Unknown"


class ActorReadSchema(ActorSchema):
    bio: str | None
    place_of_birth: str | None
    gender: str | None
    birthdate: date | None
    homepage: str | None

    @field_validator("homepage")
    def check_homepage(cls, value):
        if value is None:
            return "No home page"
        else:
            return value


class CountryReadSchema(BaseModel):
    id: int
    name: str


class CountryCreateSchema(BaseModel):
    name: str


class RatingReadSchema(BaseModel):
    id: int
    source: str
    value: str


class RatingCreateSchema(BaseModel):
    source: str
    value: str


class LanguageReadSchema(BaseModel):
    id: int
    name: str


class LanguageCreateSchema(BaseModel):
    name: str


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
