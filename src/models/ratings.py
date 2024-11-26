from pydantic import BaseModel


class RatingReadSchema(BaseModel):
    id: int
    source: str
    value: str


class RatingCreateSchema(BaseModel):
    source: str
    value: str
