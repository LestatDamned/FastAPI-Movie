from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.tables import Language
from src.models.models import LanguageSchema

router = APIRouter()


@router.get("/languages/")
async def get_languages(db: AsyncSession = Depends(get_db)) -> list[LanguageSchema]:
    result = await db.execute(select(Language))
    languages = result.scalars().all()
    return [LanguageSchema.model_validate(language, from_attributes=True) for language in languages]


@router.get("/languages/{language_id}/")
async def get_language(language_id: int, db: AsyncSession = Depends(get_db)) -> LanguageSchema:
    result = await db.execute(select(Language).filter_by(id=language_id))
    language = result.scalar_one_or_none()
    if language is None:
        HTTPException(status_code=404, detail="Language not found")
    return LanguageSchema.model_validate(language, from_attributes=True)


@router.patch("/languages/{language_id}/")
async def update_language(language_id: int, new_name: str, db: AsyncSession = Depends(get_db)) -> LanguageSchema:
    result = await db.execute(select(Language).filter_by(id=(language_id,)))
    language = result.scalar_one_or_none()
    if language is None:
        HTTPException(status_code=404, detail="Language not found")

    await db.execute(update(Language).filter_by(id=language_id).values(name=new_name))
    await db.commit()

    updated_language = await db.execute(select(Language).filter_by(id=language_id))
    updated_language = updated_language.scalar()
    return LanguageSchema.model_validate(updated_language, from_attributes=True)
