from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.db.tables import Rating
from src.models.models import RatingReadSchema, RatingCreateSchema

router = APIRouter()


@router.get("/ratings/")
async def get_rating(db: AsyncSession = Depends(get_db)) -> list[RatingReadSchema]:
    result = await db.execute(select(Rating))
    ratings = result.scalars().all()
    return [RatingReadSchema.model_validate(rating, from_attributes=True) for rating in ratings]


@router.get("/ratings/{rating_id}/")
async def get_rating(rating_id: int, db: AsyncSession = Depends(get_db)) -> RatingReadSchema:
    result = await db.execute(select(Rating).filter_by(id=rating_id))
    rating = result.scalar_one_or_none()
    if rating is None:
        raise HTTPException(status_code=404, detail="Ratings not found")
    return RatingReadSchema.model_validate(rating, from_attributes=True)


@router.put("/ratings/{rating_id}/")
async def update_rating(rating_id: int, new_data: RatingCreateSchema,
                        db: AsyncSession = Depends(get_db)) -> RatingReadSchema:
    result = await db.execute(select(Rating).filter_by(id=rating_id))
    rating = result.scalar_one_or_none()
    if rating is None:
        raise HTTPException(status_code=404, detail="Ratings not found")

    await db.execute(update(Rating).filter_by(id=rating_id).values(**new_data.model_dump(exclude_unset=True)))
    await db.commit()

    updated_rating = await db.execute(select(Rating).filter_by(id=rating_id))
    updated_rating = updated_rating.scalar()
    return RatingReadSchema.model_validate(updated_rating, from_attributes=True)
