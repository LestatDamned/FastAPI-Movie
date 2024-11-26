from pydantic import BaseModel


class GenreCreateSchema(BaseModel):
    name: str


class GenreReadSchema(BaseModel):
    id: int
    name: str
