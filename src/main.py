import os
from os import getenv
from typing import List

from fastapi import FastAPI

from app.routers.movies import router

app = FastAPI(
    title="Movies app"
)

app.include_router(
    router=router,
)
