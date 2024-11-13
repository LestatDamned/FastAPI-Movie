from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.tables import Rating
from src.models.models import RatingSchema

router = APIRouter()


@router.get("/ratings/")
async def get_rating(db: AsyncSession = Depends(get_db)) -> list[RatingSchema]:
    result = await db.execute(select(Rating))
    ratings = result.scalars().all()
    return [RatingSchema.model_validate(rating, from_attributes=True) for rating in ratings]


@router.get("/ratings/{rating_id}/")
async def get_rating(rating_id: int, db: AsyncSession = Depends(get_db)) -> RatingSchema:
    result = await db.execute(select(Rating).filter_by(id=rating_id))
    rating = result.scalar_one_or_none()
    if rating is None:
        HTTPException(status_code=404, detail="Ratings not found")
    return RatingSchema.model_validate(rating, from_attributes=True)


@router.patch("/ratings/{rating_id}/")
async def update_rating(rating_id: int, new_source: str, new_value: str,
                        db: AsyncSession = Depends(get_db)) -> RatingSchema:
    result = await db.execute(select(Rating).filter_by(id=rating_id))
    rating = result.scalar_one_or_none()
    if rating is None:
        HTTPException(status_code=404, detail="Ratings not found")

    await db.execute(update(Rating).filter_by(id=rating_id).values(source=new_source, value=new_value))
    await db.commit()

    updated_rating = await db.execute(select(Rating).filter_by(id=rating_id))
    updated_rating = updated_rating.scalar()
    return RatingSchema.model_validate(updated_rating, from_attributes=True)
