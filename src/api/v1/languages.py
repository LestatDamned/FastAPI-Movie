from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.tables import Language

router = APIRouter()


@router.get("/languages/")
async def get_languages(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Language))
    languages = result.scalars().all()
    return languages


@router.get("/languages/{language_id}/")
async def get_language(language_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Language).filter_by(id=language_id))
    language = result.scalar_one_or_none()
    if language is None:
        return {"message": "No languages"}


@router.patch("/languages/{language_id}/")
async def update_language(language_id: int, new_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Language).filter_by(id=(language_id,)))
    language = result.scalar_one_or_none()
    if language is None:
        return {"message": "No languages"}

    await db.execute(update(Language).filter_by(id=language_id).values(name=new_name))
    await db.commit()

    updated_language = await db.execute(select(Language).filter_by(id=language_id))
    updated_language = updated_language.scalar()
    return updated_language
