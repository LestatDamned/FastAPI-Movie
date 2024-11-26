from pydantic import BaseModel


class DirectorReadSchema(BaseModel):
    id: int
    name: str


class DirectorCreateSchema(BaseModel):
    name: str
