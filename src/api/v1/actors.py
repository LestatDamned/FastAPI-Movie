from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.tables import Actor
from src.models.models import ActorSchema, ActorDetailReadSchema

router = APIRouter()


@router.get("/actors/")
async def get_actor(db: AsyncSession = Depends(get_db)) -> list[ActorDetailReadSchema]:
    result = await db.execute(select(Actor))
    actors = result.scalars().all()
    return [ActorDetailReadSchema.model_validate(actor, from_attributes=True) for actor in actors]


@router.get("/actors/{actor_id}/")
async def get_actor(actor_id: int, db: AsyncSession = Depends(get_db)) -> ActorDetailReadSchema:
    result = await db.execute(select(Actor).filter_by(id=actor_id))
    actors = result.scalar_one_or_none()
    if actors is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return ActorDetailReadSchema.model_validate(actors, from_attributes=True)


@router.patch("/actors/{actor_id}/")
async def update_actor(actor_id: int, new_name: str, db: AsyncSession = Depends(get_db)) -> ActorSchema:
    result = await db.execute(select(Actor).filter_by(id=actor_id))
    actor = result.scalar_one_or_none()
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")

    query = update(Actor).filter_by(id=actor_id).values(name=new_name)
    await db.execute(query)
    await db.commit()

    updated_actor = await db.execute(select(Actor).filter_by(id=actor_id))
    updated_actor = updated_actor.scalar()
    return ActorDetailReadSchema.model_validate(updated_actor, from_attributes=True)
