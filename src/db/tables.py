from datetime import date

from sqlalchemy import Column, Integer, ForeignKey, Table, JSON, Date, String
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column

Base = declarative_base()

movie_directors_m2m = Table(
    'movie_directors_m2m', Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("director_id", Integer, ForeignKey("directors.id"), primary_key=True)
)

movie_actors_m2m = Table(
    'movie_actors_m2m', Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("actor_id", Integer, ForeignKey("actors.id"), primary_key=True)
)

movie_genres_m2m = Table(
    "movie_genres_m2m", Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True)
)
movie_writers_m2m = Table(
    "movie_writers_m2m", Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("writer_id", Integer, ForeignKey("writers.id"), primary_key=True)
)
movie_countries_m2m = Table(
    "movie_countries_m2m", Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("country_id", Integer, ForeignKey("countries.id"), primary_key=True)
)
movie_languages_m2m = Table(
    "movie_languages_m2m", Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("language_id", Integer, ForeignKey("languages.id"), primary_key=True)
)


# TODO констрейны узнать что такое, м2м чтобы ссылался подругому, составной PK, проработать с ключами
#  нейминг столбцов, поправить,
class Movie(Base):
    __tablename__ = 'movies'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    year: Mapped[int]
    release_date: Mapped[str]
    runtime: Mapped[str]
    plot: Mapped[str]
    awards: Mapped[str]
    poster: Mapped[str]
    metascore: Mapped[str]
    imdb_rating: Mapped[str]
    imdb_id: Mapped[str]
    box_office: Mapped[str]

    director: Mapped[list["Director"]] = relationship("Director",
                                                      secondary=movie_directors_m2m,
                                                      back_populates="movies")
    language: Mapped[list["Language"]] = relationship("Language",
                                                      secondary=movie_languages_m2m,
                                                      back_populates="movies")

    genres: Mapped[list["Genre"]] = relationship("Genre",
                                                 back_populates="movies",
                                                 secondary=movie_genres_m2m)
    writer: Mapped[list["Writer"]] = relationship("Writer",
                                                  secondary=movie_writers_m2m,
                                                  back_populates="movies")
    actors: Mapped[list["Actor"]] = relationship("Actor",
                                                 secondary=movie_actors_m2m,
                                                 back_populates="movies")
    country: Mapped[list["Country"]] = relationship("Country",
                                                    back_populates="movies",
                                                    secondary=movie_countries_m2m)
    ratings: Mapped[list["Rating"]] = relationship("Rating", back_populates="movie")


class Genre(Base):
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    movies: Mapped[list["Movie"]] = relationship("Movie",
                                                 secondary=movie_genres_m2m,
                                                 back_populates="genres")


class Director(Base):
    __tablename__ = 'directors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    movies: Mapped[list["Movie"]] = relationship("Movie",
                                                 back_populates="director",
                                                 secondary=movie_directors_m2m, )


class Writer(Base):
    __tablename__ = 'writers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    movies: Mapped[list["Movie"]] = relationship("Movie",
                                                 secondary=movie_writers_m2m,
                                                 back_populates="writer")


class Actor(Base):
    __tablename__ = 'actors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    bio: Mapped[str | None] = mapped_column(String, nullable=True)
    place_of_birth: Mapped[str | None] = mapped_column(String, nullable=True)
    gender: Mapped[str | None] = mapped_column(String, nullable=True)
    birthdate: Mapped[date | None] = mapped_column(Date, nullable=True)
    homepage: Mapped[str | None] = mapped_column(String, nullable=True)

    movies: Mapped[list["Movie"]] = relationship("Movie",
                                                 secondary=movie_actors_m2m,
                                                 back_populates="actors")


class Country(Base):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    movies: Mapped[list["Movie"]] = relationship("Movie",
                                                 secondary=movie_countries_m2m,
                                                 back_populates="country")


class Language(Base):
    __tablename__ = 'languages'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    movies: Mapped[list["Movie"]] = relationship("Movie",
                                                 secondary=movie_languages_m2m,
                                                 back_populates="language")


class Rating(Base):
    __tablename__ = 'ratings'

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str]
    value: Mapped[str]

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    movie: Mapped["Movie"] = relationship("Movie", back_populates="ratings")
