from pydantic import BaseModel, Field


class LoadMovieFromAPI(BaseModel):
    name: str
    year: int = Field(default=2023)

