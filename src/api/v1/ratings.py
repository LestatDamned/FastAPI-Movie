from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.base import RatingsDAO
from src.db.database import get_db
from src.models.models import RatingReadSchema, RatingCreateSchema

router = APIRouter()


@router.get("/")
async def get_rating(db: AsyncSession = Depends(get_db)) -> list[RatingReadSchema]:
    ratings = await RatingsDAO.get_all(db)
    return [RatingReadSchema.model_validate(rating, from_attributes=True) for rating in ratings]


@router.get("/{rating_id}/")
async def get_rating(rating_id: int, db: AsyncSession = Depends(get_db)) -> RatingReadSchema:
    rating = await RatingsDAO.get_by_id(rating_id, db)
    return RatingReadSchema.model_validate(rating, from_attributes=True)


@router.put("/{rating_id}/")
async def update_rating(rating_id: int, new_data: RatingCreateSchema,
                        db: AsyncSession = Depends(get_db)) -> RatingReadSchema:
    updated_rating = await RatingsDAO.update(rating_id, new_data, db)
    return RatingReadSchema.model_validate(updated_rating, from_attributes=True)
