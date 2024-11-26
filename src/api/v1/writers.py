from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.base import WritersDAO
from src.db.database import get_db
from src.models.writers import WriterReadSchema, WriterCreateSchema

router = APIRouter()


@router.get("/")
async def get_writer(db: AsyncSession = Depends(get_db)) -> list[WriterReadSchema]:
    writers = await WritersDAO.get_all(db)
    return [WriterReadSchema.model_validate(writer, from_attributes=True) for writer in writers]


@router.get("/{writer_id}/")
async def get_writer(writer_id: int, db: AsyncSession = Depends(get_db)) -> WriterReadSchema:
    writers = await WritersDAO.get_by_id(writer_id, db)
    return WriterReadSchema.model_validate(writers, from_attributes=True)


@router.put("/{writer_id}/")
async def update_writer(writer_id: int, new_data: WriterCreateSchema,
                        db: AsyncSession = Depends(get_db)) -> WriterReadSchema:
    writer = await WritersDAO.update(writer_id, new_data, db)
    return WriterReadSchema.model_validate(writer, from_attributes=True)


@router.get("/movies/{name}")
async def get_by_name(name: str, db: AsyncSession = Depends(get_db)):
    writers = await WritersDAO.get_with_movies(name, db)
    return writers
