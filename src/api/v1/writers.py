from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.tables import Writer

router = APIRouter()


@router.get("/writers/")
async def get_writer(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Writer))
    writers = result.scalars().all()
    return writers


@router.get("/writers/{writer_id}/")
async def get_writer(writer_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Writer).filter_by(id=writer_id))
    writers = result.scalar_one_or_none()
    if writers is None:
        return {"message": "No writers"}
    return writers


@router.patch("/writers/{writer_id}/")
async def update_writer(writer_id: int, new_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Writer).filter_by(id=writer_id))
    writer = result.scalar_one_or_none()
    if writer is None:
        return {"message": "No writers"}

    query = update(Writer).filter_by(id=writer_id).values(name=new_name)
    await db.execute(query)
    await db.commit()

    updated_writer = await db.execute(select(Writer).filter_by(id=writer_id))
    updated_writer = updated_writer.scalar()
    return updated_writer
