from pydantic import BaseModel


class WriterReadSchema(BaseModel):
    id: int
    name: str


class WriterCreateSchema(BaseModel):
    name: str
