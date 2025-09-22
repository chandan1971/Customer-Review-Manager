from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.review_dao import ReviewDAO
from app.schemas.review_DTO import ReviewCreateDTO
from app.schemas.review_model import ReviewModel
from app.utils.logger import get_logger
from typing import List
from fastapi import HTTPException

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
        return 0
    
    review_dicts = [review.model_dump() for review in reviews]

    try:
        db.bulk_insert_mappings(
            ReviewModel,  
            review_dicts
        )
        db.commit()
        return len(reviews)
    except Exception as e:
        db.rollback()
        logger.error("Failed to insert reviews bulk", e)
        return 0

def get_review_query(id: int):
    return text("SELECT * FROM reviews WHERE id = :id").bindparams(id=id)


def get_review_by_id(db: Session, id: int):
    query = get_review_query(id)
    try:
        result = db.execute(query).mappings().first()  
    except Exception as e:
        raise e
    if not result:
        raise HTTPException(status_code=404, detail=f"Review with ID {id} not found")
    
    return result