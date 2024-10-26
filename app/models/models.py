
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base, Mapped
from sqlalchemy.testing.schema import mapped_column

Base = declarative_base()

movie_actors = Table(
    'movie_actors', Base.metadata,
    Column("movie_id", Integer, ForeignKey("movie.id"), primary_key=True),
    Column("actor_id", Integer, ForeignKey("actor.id"), primary_key=True)
)

movie_genres = Table(
    "movie_genres", Base.metadata,
    Column("movie_id", Integer, ForeignKey("movie.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genre.id"), primary_key=True)
)
movie_writers = Table(
    "movie_writers", Base.metadata,
    Column("movie_id", Integer, ForeignKey("movie.id"), primary_key=True),
    Column("writer_id", Integer, ForeignKey("writer.id"), primary_key=True)
)
movie_countries = Table(
    "movie_countries", Base.metadata,
    Column("movie_id", Integer, ForeignKey("movie.id"), primary_key=True),
    Column("country_id", Integer, ForeignKey("country.id"), primary_key=True)
)


class Movie(Base):
    __tablename__ = 'movie'

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

    director_id: Mapped[int] = mapped_column(ForeignKey('director.id'))
    director: Mapped[list["Director"]] = relationship(back_populates="movie")
    language_id: Mapped[int] = mapped_column(ForeignKey('language.id'))
    language: Mapped[list["Language"]] = relationship(back_populates="movie")

    genres: Mapped[list["Genre"]] = relationship("Genre", back_populates="movie", secondary="movie_genres")
    writer: Mapped[list["Writer"]] = relationship(secondary="movie_writers", back_populates="movie")
    actors: Mapped[list["Actor"]] = relationship(secondary="movie_actors", back_populates="movie")
    country: Mapped[list["Country"]] = relationship(back_populates="movie", secondary="movie_countries")
    ratings: Mapped[list["Rating"]] = relationship(back_populates="movie")


class Genre(Base):
    __tablename__ = 'genre'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    movies: Mapped[list["Movie"]] = relationship("Movie", secondary=movie_genres, back_populates="genre")


class Director(Base):
    __tablename__ = 'director'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    movies: Mapped[list["Movie"]] = relationship(back_populates="director")


class Writer(Base):
    __tablename__ = 'writer'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    movies: Mapped[list["Movie"]] = relationship("Movie", secondary=movie_writers, back_populates="writer")


class Actor(Base):
    __tablename__ = 'actor'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    movies: Mapped[list["Movie"]] = relationship("Movie", secondary=movie_actors, back_populates="actor")


class Country(Base):
    __tablename__ = 'country'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    movies: Mapped[list["Movie"]] = relationship("Movie", secondary=movie_countries, back_populates="country")


class Language(Base):
    __tablename__ = 'language'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    movies: Mapped[list["Movie"]] = relationship("Movie", back_populates="language")


class Rating(Base):
    __tablename__ = 'rating'

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str]
    value: Mapped[str]

    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id"))
    movie: Mapped[list["Movie"]] = relationship("Movie", back_populates="rating")
