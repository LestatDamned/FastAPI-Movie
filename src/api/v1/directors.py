from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.base import DirectorsDAO
from src.db.database import get_db
from src.models.directors import DirectorReadSchema, DirectorCreateSchema

router = APIRouter()


@router.get("/")
async def get_director(db: AsyncSession = Depends(get_db)) -> list[DirectorReadSchema]:
    directors = await DirectorsDAO.get_all(db)
    return [DirectorReadSchema.model_validate(director, from_attributes=True) for director in directors]


@router.get("/{director_id}")
async def get_director(director_id: int, db: AsyncSession = Depends(get_db)) -> DirectorReadSchema:
    director = await DirectorsDAO.get_by_id(director_id, db)
    return DirectorReadSchema.model_validate(director, from_attributes=True)


@router.put("/{director_id}")
async def update_director(director_id: int, new_data: DirectorCreateSchema,
                          db: AsyncSession = Depends(get_db)) -> DirectorReadSchema:
    updated_director = await DirectorsDAO.update(director_id, new_data, db)
    return DirectorReadSchema.model_validate(updated_director, from_attributes=True)


@router.get("/movies/{name}")
async def get_by_name(name: str, db: AsyncSession = Depends(get_db)):
    directors = await DirectorsDAO.get_with_movies(name, db)
    return directors
