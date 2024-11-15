from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.db.database import get_db
from src.db.tables import Actor, Movie
from src.models.models import ActorReadSchema, MovieReadSchema, ActorCreateSchema

router = APIRouter()


@router.get("/actors/")
async def get_actor(db: AsyncSession = Depends(get_db)) -> list[ActorReadSchema]:
    result = await db.execute(select(Actor))
    actors = result.scalars().all()
    return [ActorReadSchema.model_validate(actor, from_attributes=True) for actor in actors]


@router.get("/actors/{actor_id}/")
async def get_actor(actor_id: int, db: AsyncSession = Depends(get_db)) -> ActorReadSchema:
    result = await db.execute(select(Actor).filter_by(id=actor_id))
    actors = result.scalar_one_or_none()
    if actors is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return ActorReadSchema.model_validate(actors, from_attributes=True)


@router.put("/actors/{actor_id}/")
async def update_actor(actor_id: int, new_data: ActorCreateSchema,
                       db: AsyncSession = Depends(get_db)) -> ActorReadSchema:
    result = await db.execute(select(Actor).filter_by(id=actor_id))
    actor = result.scalar_one_or_none()
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")

    query = update(Actor).filter_by(id=actor_id).values(**new_data.model_dump(exclude_unset=True))
    await db.execute(query)
    await db.commit()

    updated_actor = await db.execute(select(Actor).filter_by(id=actor_id))
    updated_actor = updated_actor.scalar()
    return ActorReadSchema.model_validate(updated_actor, from_attributes=True)


@router.post("/movies/with_actor/{actor_name}/")
async def get_movie_with_actor(actor_name: str, db: AsyncSession = Depends(get_db)) -> list[MovieReadSchema]:
    search_actor_name = await db.execute(select(Actor).filter(Actor.name.ilike(f"%{actor_name}%")))
    search_actor_name = search_actor_name.scalar_one_or_none()
    if search_actor_name is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    query = (select(Movie).join(Movie.actors).filter_by(id=search_actor_name.id)
             .options(joinedload(Movie.actors),
                      joinedload(Movie.director),
                      joinedload(Movie.language),
                      joinedload(Movie.genres),
                      joinedload(Movie.writer),
                      joinedload(Movie.country),
                      joinedload(Movie.ratings)))
    result = await db.execute(query)
    movies = result.unique().scalars().all()
    return [MovieReadSchema.model_validate(movie, from_attributes=True) for movie in movies]
