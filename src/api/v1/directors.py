from fastapi import Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.tables import Director

router = APIRouter()


@router.get("/directors/")
async def get_director(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Director))
    director = result.scalars().all()
    return director


@router.get("/directors/{director_id}")
async def get_director(director_id: int, db: AsyncSession = Depends(get_db)):
    query = (select(Director).filter_by(id=director_id))
    db_movie = await db.execute(query)
    db_movie = db_movie.scalar()
    return db_movie


@router.patch("/directors/{director_id}")
async def update_director(director_id: int, new_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Director).filter_by(id=director_id))
    movie = result.scalar_one_or_none()
    if movie is None:
        return {"Message": "Director not found."}
    query = update(Director).filter_by(id=director_id).values(name=new_name)
    await db.execute(query)
    await db.commit()

    updated_movie = await db.execute(select(Director).filter_by(id=director_id))
    updated_movie = updated_movie.scalar()
    return updated_movie
