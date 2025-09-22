from sqlalchemy.orm import Session
from app.schemas.review_dao import ReviewDAO
from app.schemas.review_DTO import ReviewCreateDTO
from app.utils.db_utils import insert_reviews_bulk
from app.utils.logger import get_logger
from app.utils.db_utils import dao_to_dto
from app.utils.db_utils import get_review_by_id
from app.schemas.review_model import ReviewModel
from sqlalchemy import or_
from app.schemas.review_filter_request_dto import ReviewFilterRequest
from app.utils.filter_util import normalize_filter

logger = get_logger(__name__)

class ReviewService:
    def __init__(self, db: Session):
        self.db = db

    def ingest_reviews(self, reviews: list[ReviewDAO]) -> int:
        reviews_dto: list[ReviewCreateDTO] = []
        for review in reviews:
            review_dto: ReviewCreateDTO =dao_to_dto(review)
            reviews_dto.append(review_dto)
        rows_inserted = insert_reviews_bulk(self.db, reviews_dto)
        return rows_inserted
    
    def get_review_by_id(self, id:int):
        return get_review_by_id(self.db,id)
    
    def get_reviews(self, filters: ReviewFilterRequest):
        query = self.db.query(ReviewModel)
        location = normalize_filter(filters.location)
        sentiment = normalize_filter(filters.sentiment)
        q = normalize_filter(filters.q)

        
        if location:
            query = query.filter(ReviewModel.location.ilike(f"%{location}%"))

        if sentiment :
            query = query.filter(ReviewModel.review_text.ilike(f"%{sentiment}%"))

        if q:
            or_filters = []
            if q:
                or_filters.append(ReviewModel.review_text.ilike(f"%{q}%"))
                or_filters.append(ReviewModel.location.ilike(f"%{q}%"))

            if or_filters:
                query = query.filter(or_(*or_filters))

        
        total = query.count()
        results = query.offset((filters.page - 1) * filters.page_size).limit(filters.page_size).all()

        
        return {
            "total": total,
            "page": filters.page,
            "page_size": filters.page_size,
            "reviews": results
        }

