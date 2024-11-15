from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.tables import Director
from src.models.models import DirectorReadSchema, DirectorCreateSchema

router = APIRouter()


@router.get("/directors/")
async def get_director(db: AsyncSession = Depends(get_db)) -> list[DirectorReadSchema]:
    result = await db.execute(select(Director))
    directors = result.scalars().all()
    return [DirectorReadSchema.model_validate(director, from_attributes=True) for director in directors]


@router.get("/directors/{director_id}")
async def get_director(director_id: int, db: AsyncSession = Depends(get_db)) -> DirectorReadSchema:
    query = (select(Director).filter_by(id=director_id))
    result = await db.execute(query)
    director = result.scalar_one_or_none()
    if director is None:
        raise HTTPException(status_code=404, detail="Director not found")
    return DirectorReadSchema.model_validate(director, from_attributes=True)


@router.put("/directors/{director_id}")
async def update_director(director_id: int, new_data: DirectorCreateSchema,
                          db: AsyncSession = Depends(get_db)) -> DirectorReadSchema:
    result = await db.execute(select(Director).filter_by(id=director_id))
    director = result.scalar_one_or_none()
    if director is None:
        raise HTTPException(status_code=404, detail="Director not found")
    query = update(Director).filter_by(id=director_id).values(**new_data.model_dump(exclude_unset=True))
    await db.execute(query)
    await db.commit()

    updated_director = await db.execute(select(Director).filter_by(id=director_id))
    updated_director = updated_director.scalar()
    return DirectorReadSchema.model_validate(updated_director, from_attributes=True)
