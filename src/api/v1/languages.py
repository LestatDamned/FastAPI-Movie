from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.base import LanguagesDAO
from src.db.database import get_db
from src.models.models import LanguageReadSchema, LanguageCreateSchema

router = APIRouter()


@router.get("/")
async def get_languages(db: AsyncSession = Depends(get_db)) -> list[LanguageReadSchema]:
    languages = await LanguagesDAO.get_all(db)
    return [LanguageReadSchema.model_validate(language, from_attributes=True) for language in languages]


@router.get("/{language_id}/")
async def get_language(language_id: int, db: AsyncSession = Depends(get_db)) -> LanguageReadSchema:
    language = await LanguagesDAO.get_by_id(language_id, db)
    return LanguageReadSchema.model_validate(language, from_attributes=True)


@router.put("/{language_id}/")
async def update_language(language_id: int, new_data: LanguageCreateSchema,
                          db: AsyncSession = Depends(get_db)) -> LanguageReadSchema:
    updated_language = await LanguagesDAO.update(language_id, new_data, db)
    return LanguageReadSchema.model_validate(updated_language, from_attributes=True)
