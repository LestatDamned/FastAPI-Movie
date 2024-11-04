from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.tables import Country

router = APIRouter()


@router.get("/countries/")
async def get_country(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country))
    countries = result.scalars().all()
    return countries


@router.get("/countries/{country_id}/")
async def get_country(country_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country).filter_by(id=country_id))
    countries = result.scalar_one_or_none()
    if countries is None:
        return {"message": "No countries"}
    return countries


@router.patch("/countries/{country_id}/")
async def update_country(country_id: int, new_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country).filter_by(id=country_id))
    country = result.scalar_one_or_none()
    if country is None:
        return {"message": "No countries"}

    await db.execute(update(Country).filter_by(id=country_id).values(name=new_name))
    await db.commit()

    updated_country = await db.execute(select(Country).filter_by(id=country_id))
    updated_country = updated_country.scalar()
    return updated_country
