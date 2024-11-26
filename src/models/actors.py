from datetime import date

from pydantic import BaseModel, Field, field_validator


class ActorSchema(BaseModel):
    name: str


class ActorCreateSchema(ActorSchema):
    bio: str | None = Field(alias="biography")
    place_of_birth: str | None = Field()
    gender: str | None = Field(description="Gender send 1 for Woman, send 2 for Man")
    birthdate: date | None = Field(alias="birthday")
    homepage: str | None = Field(alias="homepage")

    @field_validator("gender", mode="before")
    def convert_gender(cls, value):
        if value == 1:
            return "Woman"
        elif value == 2:
            return "Male"
        else:
            return "Unknown"


class ActorReadSchema(ActorSchema):
    bio: str | None
    place_of_birth: str | None
    gender: str | None
    birthdate: date | None
    homepage: str | None

    @field_validator("homepage")
    def check_homepage(cls, value):
        if value is None:
            return "No home page"
        else:
            return value
