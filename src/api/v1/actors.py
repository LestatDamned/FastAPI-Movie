from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.base import ActorDAO
from src.db.database import get_db
from src.models.models import ActorReadSchema, MovieReadSchema, ActorCreateSchema

router = APIRouter()


@router.get("/")
async def get_actor(db: AsyncSession = Depends(get_db)) -> list[ActorReadSchema]:
    actors = await ActorDAO.get_all(db)
    return [ActorReadSchema.model_validate(actor, from_attributes=True) for actor in actors]


@router.get("/{actor_id}/")
async def get_actor(actor_id: int, db: AsyncSession = Depends(get_db)) -> ActorReadSchema:
    actors = await ActorDAO.get_by_id(actor_id, db)
    return ActorReadSchema.model_validate(actors, from_attributes=True)


@router.put("/{actor_id}/")
async def update_actor(actor_id: int, new_data: ActorCreateSchema,
                       db: AsyncSession = Depends(get_db)) -> ActorReadSchema:
    updated_actor = await ActorDAO.update(actor_id, new_data, db)
    return ActorReadSchema.model_validate(updated_actor, from_attributes=True)


@router.post("/movies/{actor_name}/")
async def get_movie_with_actor(actor_name: str, db: AsyncSession = Depends(get_db)) -> list[MovieReadSchema]:
    movies = await ActorDAO.get_movie_with_actor(actor_name, db)
    return [MovieReadSchema.model_validate(movie, from_attributes=True) for movie in movies]
