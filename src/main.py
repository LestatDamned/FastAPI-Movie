from fastapi import FastAPI

from src.api.movies import router

app = FastAPI(
    title="Movies src"
)

app.include_router(
    router=router,
)
