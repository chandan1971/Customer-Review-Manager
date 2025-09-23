from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.review_dao import ReviewDAO
from app.schemas.review_DTO import ReviewCreateDTO
from app.schemas.review_model import ReviewModel
from app.utils.logger import get_logger
from typing import List
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

logger = get_logger(__name__)

def dao_to_dto(dao: ReviewDAO) -> ReviewCreateDTO:
    return ReviewCreateDTO(
        id=dao.id,
        location=dao.location,
        rating=dao.rating,
        review_text=dao.text,
        review_date=dao.date
    )

def insert_reviews_bulk(db: Session, reviews: List[ReviewCreateDTO]) -> int:
    if not reviews:
        logger.info("No reviews provided for bulk insert")
        return 0
    
    review_dicts = [review.model_dump() for review in reviews]

    try:
        db.bulk_insert_mappings(ReviewModel, review_dicts)
        db.flush()  
        logger.info(f"Prepared {len(reviews)} reviews for insert")
        return len(reviews)
    except Exception as e:
        logger.error("Failed to insert reviews bulk", exc_info=True)
        raise
  

def get_review_query(id: int):
    return text("SELECT * FROM reviews WHERE id = :id").bindparams(id=id)

def get_review_by_id(db: Session, id: int):
    query = get_review_query(id)
    try:
        result = db.execute(query).mappings().first()
        if not result:
            raise HTTPException(status_code=404, detail=f"Review with ID {id} not found")
        return result
    except Exception as e:
        logger.error(f"Error fetching review with ID {id}", exc_info=True)
        raise
