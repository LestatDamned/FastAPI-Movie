from fastapi import FastAPI

from src.api.routers import router as api_router

app = FastAPI(
    title="Movies src"
)

app.include_router(api_router)
