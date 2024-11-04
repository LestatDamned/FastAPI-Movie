from fastapi import FastAPI

from src.api.v1 import movies, actors, countries, directors, genres, languages, ratings, writers

app = FastAPI(
    title="Movies src"
)

app.include_router(movies.router)
app.include_router(actors.router)
app.include_router(countries.router)
app.include_router(directors.router)
app.include_router(genres.router)
app.include_router(languages.router)
app.include_router(ratings.router)
app.include_router(writers.router)
