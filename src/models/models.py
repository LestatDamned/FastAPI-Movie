from datetime import date

from pydantic import BaseModel, Field, field_validator


class GenreSchema(BaseModel):
    name: str


class DirectorSchema(BaseModel):
    name: str


class WriterSchema(BaseModel):
    name: str


class ActorSchema(BaseModel):
    name: str


class ActorDetailSchema(ActorSchema):
    bio: str | None = Field(alias="biography")
    place_of_birth: str | None = Field()
    gender: str | None = Field()
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


class ActorDetailReadSchema(ActorDetailSchema):
    bio: str | None
    place_of_birth: str | None
    gender: str | None
    birthdate: date | None
    homepage: str | None


class CountrySchema(BaseModel):
    name: str


class RatingSchema(BaseModel):
    source: str
    value: str


class LanguageSchema(BaseModel):
    name: str


class MovieSchema(BaseModel):
    Title: str = Field(alias="title")
    Year: int = Field(alias="year")
    Released: str = Field(alias="release_date")
    Runtime: str = Field(alias="runtime")
    Genre: list[GenreSchema] = Field(alias="genres")
    Director: list[DirectorSchema] = Field(alias="director")
    Writer: list[WriterSchema] = Field(alias="writer")
    Actors: list[ActorSchema] = Field(alias="actors")
    Plot: str = Field(alias="plot")
    Language: list[LanguageSchema] = Field(alias="language")
    Country: list[CountrySchema] = Field(alias="country")
    Awards: str = Field(alias="awards")
    Poster: str = Field(alias="poster")
    Ratings: list[RatingSchema] = Field(alias="ratings")
    Metascore: str = Field(alias="metascore")
    imdbRating: str = Field(alias="imdb_rating")
    imdbID: str = Field(alias="imdb_id")
    BoxOffice: str = Field(alias="box_office")


class MovieSchemaWrite(BaseModel):
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
