from fastapi import APIRouter

from src.api.v1 import movies, actors, countries, directors, genres, languages, ratings, writers, load_movies

router = APIRouter()

router.include_router(movies.router, prefix="/movies", tags=["Фильмы"])
router.include_router(actors.router, prefix="/actors", tags=["Актеры"])
router.include_router(countries.router, prefix="/countries", tags=["Страны"])
router.include_router(directors.router, prefix="/directors", tags=["Режиссеры"])
router.include_router(genres.router, prefix="/genres", tags=["Жанры"])
router.include_router(languages.router, prefix="/languages", tags=["Языки"])
router.include_router(ratings.router, prefix="/ratings", tags=["Рейтинги"])
router.include_router(writers.router, prefix="/writers", tags=["Сценаристы"])
router.include_router(load_movies.router, prefix="/load", tags=["Загрузка фильмов в БД"])