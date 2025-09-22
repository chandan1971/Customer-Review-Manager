from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.review_dao import ReviewDAO
from app.schemas.review_DTO import ReviewCreateDTO
from app.schemas.review_model import ReviewModel
from app.constants.db_constants import REVIEWS_TABLE
from app.utils.logger import get_logger
from pydantic import BaseModel
from datetime import datetime
from typing import List

logger = get_logger(__name__)

def dao_to_dto(dao: ReviewDAO) -> ReviewCreateDTO:
    return ReviewCreateDTO(
        id=dao.id,
        location=dao.location,
        rating=dao.rating,
        review_text=dao.text,
        review_date=dao.date
    )

def build_insert_query(table_name: str, dto: BaseModel):
    data = dto.model_dump()
    if isinstance(data.get("review_date"), str):
        data["review_date"] = datetime.strptime(data["review_date"], "%Y-%m-%d").date()
    columns = ", ".join([f'"{key}"' for key in data.keys()])
    placeholders = ", ".join([f":{key}" for key in data.keys()])
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    return query, data

def insert_reviews(db: Session, reviews: List[ReviewDAO]) -> int:
    rows_inserted = 0
    for review in reviews:
        logger.info(f"Inserting review: {review}")
        review_dto = dao_to_dto(review)
        query_str, params = build_insert_query(REVIEWS_TABLE, review_dto)
        query_text = text(query_str)  
        logger.info(f"Query: {query_text}")
        logger.info(f"Params: {params}")
        try:
            db.execute(query_text, params)
            db.commit()
            rows_inserted += 1
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to insert review {review.id}: {e}")
    return rows_inserted

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
        logger.error("Failed to insert reviews bulk", exc_info=e)
        return 0
