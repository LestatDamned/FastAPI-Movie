from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.base import CountriesDAO
from src.db.database import get_db
from src.models.countries import CountryReadSchema, CountryCreateSchema

router = APIRouter()


@router.get("/")
async def get_country(db: AsyncSession = Depends(get_db)) -> list[CountryReadSchema]:
    countries = await CountriesDAO.get_all(db)
    return [CountryReadSchema.model_validate(country, from_attributes=True) for country in countries]


@router.get("/{country_id}/")
async def get_country(country_id: int, db: AsyncSession = Depends(get_db)) -> CountryReadSchema:
    countries = await CountriesDAO.get_by_id(country_id, db)
    return CountryReadSchema.model_validate(countries, from_attributes=True)


@router.put("/{country_id}/")
async def update_country(country_id: int, new_data: CountryCreateSchema,
                         db: AsyncSession = Depends(get_db)) -> CountryReadSchema:
    updated_country = await CountriesDAO.update(country_id, new_data, db)
    return CountryReadSchema.model_validate(updated_country, from_attributes=True)


@router.get("/movies/{name}")
async def get_by_name(name: str, db: AsyncSession = Depends(get_db)):
    countries = await CountriesDAO.get_with_movies(name, db)
    return countries
