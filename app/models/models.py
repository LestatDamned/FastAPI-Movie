from typing import List

from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base, Mapped
from sqlalchemy.testing.schema import mapped_column

Base = declarative_base()

movie_actors = Table(
    'movie_actors', Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("actor_id", Integer, ForeignKey("actors.id"), primary_key=True)
)

movie_genres = Table(
    "movie_genres", Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True)
)
movie_writers = Table(
    "movie_writers", Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("writer_id", Integer, ForeignKey("writers.id"), primary_key=True)
)
movie_countries = Table(
    "movie_countries", Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("country_id", Integer, ForeignKey("countries.id"), primary_key=True)
)


class Movie(Base):
    __tablename__ = 'movies'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    year: Mapped[int]
    release_date: Mapped[str]
    runtime: Mapped[str]

    genres: Mapped[List["Genre"]] = relationship(back_populates="movie")

    director_id: Mapped[int] = mapped_column(ForeignKey('directors.id'))
    director: Mapped["Director"] = relationship(back_populates="movies")

    writer: Mapped[List["Writer"]] = relationship(secondary="movie_writers", back_populates="movies")

    actors: Mapped[List["Actor"]] = relationship(secondary="movie_actors", back_populates="movies")

    plot: Mapped[str]

    language_id: Mapped[int] = mapped_column(ForeignKey('languages.id'))
    language: Mapped["Language"] = relationship(back_populates="movies")

    country: Mapped[List["Country"]] = relationship(back_populates="movies", secondary="movie_countries")

    awards: Mapped[str]
    poster: Mapped[str]

    ratings: Mapped["Rating"] = relationship(back_populates="movies")

    metascore: Mapped[str]
    imdb_rating: Mapped[str]
    imdb_id: Mapped[str]
    box_office: Mapped[str]


class Genre(Base):
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    movies = relationship("Movie", secondary=movie_genres, back_populates="genres")


class Director(Base):
    __tablename__ = 'directors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    movies: Mapped[list["Movie"]] = relationship(back_populates="director")


class Writer(Base):
    __tablename__ = 'writers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    movies = relationship("Movie", secondary=movie_writers, back_populates="writers")


class Actor(Base):
    __tablename__ = 'actors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    movies = relationship("Movie", secondary=movie_actors, back_populates="actors")


class Country(Base):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    movies = relationship("Movie", secondary=movie_countries, back_populates="countries")


class Language(Base):
    __tablename__ = 'languages'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    movies = relationship("Movie", back_populates="languages")


class Rating(Base):
    __tablename__ = 'ratings'

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str]
    value: Mapped[str]

    movie_id = Column(Integer, ForeignKey("movies.id"))
    movie = relationship("Movie", back_populates="ratings")
