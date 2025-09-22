from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.review_dao import ReviewDAO
from app.services.review_service import ReviewService
from app.schemas.review_filter_request_dto import ReviewFilterRequest

class ReviewController:
    def __init__(self, db: Session):
        self.service = ReviewService(db)

    def ingest_review(self, reviews: list[ReviewDAO]):
        try:
            rows_inserted = self.service.ingest_reviews(reviews)
            return {"rows_inserted": rows_inserted}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def get_review_by_id(self, id: int):
        if not isinstance(id, int) or id <= 0:
            raise HTTPException(status_code=400, detail="Invalid review ID")
        try:
            review = self.service.get_review_by_id(id)
            return {"review": review}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def get_reviews(self, filters: ReviewFilterRequest):
        if filters.page <= 0:
            raise HTTPException(status_code=400, detail="Page must be >= 1")
        if filters.page_size <= 0 or filters.page_size > 100:
            raise HTTPException(status_code=400, detail="Page size must be between 1 and 100")
        
        return self.service.get_reviews(filters)
