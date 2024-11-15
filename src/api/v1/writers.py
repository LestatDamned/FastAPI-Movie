from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.tables import Writer
from src.models.models import WriterReadSchema, WriterCreateSchema

router = APIRouter()


@router.get("/writers/")
async def get_writer(db: AsyncSession = Depends(get_db)) -> list[WriterReadSchema]:
    result = await db.execute(select(Writer))
    writers = result.scalars().all()
    return [WriterReadSchema.model_validate(writer, from_attributes=True) for writer in writers]


@router.get("/writers/{writer_id}/")
async def get_writer(writer_id: int, db: AsyncSession = Depends(get_db)) -> WriterReadSchema:
    result = await db.execute(select(Writer).filter_by(id=writer_id))
    writers = result.scalar_one_or_none()
    if writers is None:
        raise HTTPException(status_code=404, detail="Writer not found")
    return WriterReadSchema.model_validate(writers, from_attributes=True)


@router.put("/writers/{writer_id}/")
async def update_writer(writer_id: int, new_data: WriterCreateSchema,
                        db: AsyncSession = Depends(get_db)) -> WriterReadSchema:
    result = await db.execute(select(Writer).filter_by(id=writer_id))
    writer = result.scalar_one_or_none()
    if writer is None:
        raise HTTPException(status_code=404, detail="Writer not found")

    query = update(Writer).filter_by(id=writer_id).values(**new_data.model_dump(exclude_unset=True))
    await db.execute(query)
    await db.commit()

    updated_writer = await db.execute(select(Writer).filter_by(id=writer_id))
    updated_writer = updated_writer.scalar()
    return WriterReadSchema.model_validate(updated_writer, from_attributes=True)
