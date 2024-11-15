from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.tables import Country
from src.models.models import CountryReadSchema, CountryCreateSchema

router = APIRouter()


@router.get("/countries/")
async def get_country(db: AsyncSession = Depends(get_db)) -> list[CountryReadSchema]:
    result = await db.execute(select(Country))
    countries = result.scalars().all()
    return [CountryReadSchema.model_validate(country, from_attributes=True) for country in countries]


@router.get("/countries/{country_id}/")
async def get_country(country_id: int, db: AsyncSession = Depends(get_db)) -> CountryReadSchema:
    result = await db.execute(select(Country).filter_by(id=country_id))
    countries = result.scalar_one_or_none()
    if countries is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return CountryReadSchema.model_validate(countries, from_attributes=True)


@router.put("/countries/{country_id}/")
async def update_country(country_id: int, new_data: CountryCreateSchema,
                         db: AsyncSession = Depends(get_db)) -> CountryReadSchema:
    result = await db.execute(select(Country).filter_by(id=country_id))
    country = result.scalar_one_or_none()
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")

    await db.execute(update(Country).filter_by(id=country_id).values(**new_data.model_dump(exclude_unset=True)))
    await db.commit()

    updated_country = await db.execute(select(Country).filter_by(id=country_id))
    updated_country = updated_country.scalar()
    return CountryReadSchema.model_validate(updated_country, from_attributes=True)
