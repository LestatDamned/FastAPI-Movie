from pydantic import BaseModel


class CountryReadSchema(BaseModel):
    id: int
    name: str


class CountryCreateSchema(BaseModel):
    name: str
