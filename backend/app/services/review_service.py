from sqlalchemy.orm import Session
from app.schemas.review_DTO import ReviewCreateDTO
from app.utils.db_utils import insert_reviews
from app.utils.logger import get_logger
logger = get_logger(__name__)

class ReviewService:
    def __init__(self, db: Session):
        self.db = db

    def ingest_reviews(self, reviews: list[ReviewCreateDTO]) -> int:
        rows_inserted = 0
        for review in reviews:
            try:
                inserted = insert_reviews(self.db, review)  
                rows_inserted += inserted
            except Exception as e:
                logger.error(f"Failed to insert review {review.id}: {str(e)}")
        return rows_inserted
