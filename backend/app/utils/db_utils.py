from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.review_dao import ReviewDAO
from app.schemas.review_DTO import ReviewCreateDTO
from app.schemas.review_model import ReviewModel
from app.utils.logger import get_logger
from typing import List
from fastapi import HTTPException

logger = get_logger(__name__)

def dao_to_dto(dao: ReviewDAO, sentiment: str, topics: str) -> ReviewCreateDTO:
    return ReviewCreateDTO(
        id=dao.id,
        location=dao.location,
        rating=dao.rating,
        review_text=dao.text,
        review_date=dao.date,
        sentiment=sentiment,
        topics=topics
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

def get_analytics_query():
    return text("""
        SELECT topic, sentiment, COUNT(*) AS count
        FROM reviews, jsonb_array_elements_text(topics::jsonb) AS topic
        GROUP BY topic, sentiment;
    """)

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

def fetch_topic_sentiment_counts(db: Session):
    try:
        query = get_analytics_query()
        result = db.execute(query).mappings().all()
        logger.info(f"Fetched {len(result)} rows for topic-sentiment counts")
        return result
    except Exception as e:
        logger.error("Failed to fetch topic-sentiment counts", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching analytics")
