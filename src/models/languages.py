from pydantic import BaseModel


class LanguageReadSchema(BaseModel):
    id: int
    name: str


class LanguageCreateSchema(BaseModel):
    name: str
