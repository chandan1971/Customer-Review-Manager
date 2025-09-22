from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.review_dao import ReviewDAO
from app.services.review_service import ReviewService

class ReviewController:
    def __init__(self, db: Session):
        self.service = ReviewService(db)

    def ingest_review(self, reviews: list[ReviewDAO]):
        try:
            rows_inserted = self.service.ingest_reviews(reviews)
            return {"rows_inserted": rows_inserted}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
