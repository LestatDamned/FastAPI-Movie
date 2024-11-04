from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.tables import Actor

router = APIRouter()


@router.get("/actors/")
async def get_actor(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Actor))
    actors = result.scalars().all()
    return actors


@router.get("/actors/{actor_id}/")
async def get_actor(actor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Actor).filter_by(id=actor_id))
    actors = result.scalar_one_or_none()
    if actors is None:
        return {"message": "No actors"}
    return actors


@router.patch("/actors/{actor_id}/")
async def update_actor(actor_id: int, new_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Actor).filter_by(id=actor_id))
    actor = result.scalar_one_or_none()
    if actor is None:
        return {"message": "No actors"}

    query = update(Actor).filter_by(id=actor_id).values(name=new_name)
    await db.execute(query)
    await db.commit()

    updated_actor = await db.execute(select(Actor).filter_by(id=actor_id))
    updated_actor = updated_actor.scalar()
    return updated_actor
