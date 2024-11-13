from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.tables import Country
from src.models.models import CountrySchema

router = APIRouter()


@router.get("/countries/")
async def get_country(db: AsyncSession = Depends(get_db)) -> list[CountrySchema]:
    result = await db.execute(select(Country))
    countries = result.scalars().all()
    return [CountrySchema.model_validate(country, from_attributes=True) for country in countries]


@router.get("/countries/{country_id}/")
async def get_country(country_id: int, db: AsyncSession = Depends(get_db)) -> CountrySchema:
    result = await db.execute(select(Country).filter_by(id=country_id))
    countries = result.scalar_one_or_none()
    if countries is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return CountrySchema.model_validate(countries, from_attributes=True)


@router.patch("/countries/{country_id}/")
async def update_country(country_id: int, new_name: str, db: AsyncSession = Depends(get_db)) -> CountrySchema:
    result = await db.execute(select(Country).filter_by(id=country_id))
    country = result.scalar_one_or_none()
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")

    await db.execute(update(Country).filter_by(id=country_id).values(name=new_name))
    await db.commit()

    updated_country = await db.execute(select(Country).filter_by(id=country_id))
    updated_country = updated_country.scalar()
    return CountrySchema.model_validate(updated_country, from_attributes=True)
