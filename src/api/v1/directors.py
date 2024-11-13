from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.tables import Director
from src.models.models import DirectorSchema

router = APIRouter()


@router.get("/directors/")
async def get_director(db: AsyncSession = Depends(get_db)) -> list[DirectorSchema]:
    result = await db.execute(select(Director))
    directors = result.scalars().all()
    return [DirectorSchema.model_validate(director, from_attributes=True) for director in directors]


@router.get("/directors/{director_id}")
async def get_director(director_id: int, db: AsyncSession = Depends(get_db)) -> DirectorSchema:
    query = (select(Director).filter_by(id=director_id))
    result = await db.execute(query)
    director = result.scalar_one_or_none()
    if director is None:
        HTTPException(status_code=404, detail="Director not found")
    return DirectorSchema.model_validate(director, from_attributes=True)


@router.patch("/directors/{director_id}")
async def update_director(director_id: int, new_name: str, db: AsyncSession = Depends(get_db)) -> DirectorSchema:
    result = await db.execute(select(Director).filter_by(id=director_id))
    director = result.scalar_one_or_none()
    if director is None:
        HTTPException(status_code=404, detail="Director not found")
    query = update(Director).filter_by(id=director_id).values(name=new_name)
    await db.execute(query)
    await db.commit()

    updated_director = await db.execute(select(Director).filter_by(id=director_id))
    updated_director = updated_director.scalar()
    return DirectorSchema.model_validate(updated_director, from_attributes=True)
