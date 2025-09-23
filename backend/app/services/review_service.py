from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException
from transformers import pipeline
from app.schemas.review_dao import ReviewDAO
from app.schemas.review_DTO import ReviewCreateDTO
from app.schemas.review_model import ReviewModel
from app.schemas.review_filter_request_dto import ReviewFilterRequest
from app.schemas.review_reply_dto import ReviewReplyResponse
from app.constants.sentiment_enum import Sentiment
from app.utils.db_utils import insert_reviews_bulk, dao_to_dto, get_review_by_id
from app.utils.filter_util import normalize_filter
from app.utils.logger import get_logger

logger = get_logger(__name__)

class ReviewService:
    def __init__(self, db: Session):
        self.db = db

    def ingest_reviews(self, reviews: list[ReviewDAO]) -> int:
        try:
            reviews_dto: list[ReviewCreateDTO] = [dao_to_dto(r) for r in reviews]
            rows_inserted = insert_reviews_bulk(self.db, reviews_dto)
            return rows_inserted
        except Exception as e:
            logger.error("Failed to ingest reviews", exc_info=e)
            raise HTTPException(status_code=500, detail="Failed to ingest reviews")

    def get_review_by_id(self, id: int):
        try:
            review = get_review_by_id(self.db, id)
            return review
        except HTTPException:
            raise 
        except Exception as e:
            logger.error(f"Failed to fetch review with ID {id}", exc_info=e)
            raise HTTPException(status_code=500, detail="Failed to fetch review")

    def get_reviews(self, filters: ReviewFilterRequest):
        try:
            query = self.db.query(ReviewModel)
            location = normalize_filter(filters.location)
            sentiment = normalize_filter(filters.sentiment)
            q = normalize_filter(filters.q)

            if location:
                query = query.filter(ReviewModel.location.ilike(f"%{location}%"))
            if sentiment:
                query = query.filter(ReviewModel.review_text.ilike(f"%{sentiment}%"))
            if q:
                or_filters = [ReviewModel.review_text.ilike(f"%{q}%"),
                              ReviewModel.location.ilike(f"%{q}%")]
                query = query.filter(or_(*or_filters))

            total = query.count()
            results = query.offset((filters.page - 1) * filters.page_size)\
                           .limit(filters.page_size).all()

            return {
                "total": total,
                "page": filters.page,
                "page_size": filters.page_size,
                "reviews": results
            }
        except Exception as e:
            logger.error("Failed to fetch reviews with filters", exc_info=e)
            raise HTTPException(status_code=500, detail="Failed to fetch reviews")

    def suggest_reply(self, review):
        try:
            review_text = review.review_text
            sentiment_pipe = pipeline("sentiment-analysis")
            sentiment_label = sentiment_pipe(review_text)[0]["label"]
            sentiment_enum = Sentiment[sentiment_label]
            reply = sentiment_enum.default_reply()

            return ReviewReplyResponse(
                reply=reply,
                tags=[sentiment_label.lower()]
            )
        except KeyError:
            logger.warning(f"Unknown sentiment returned for review ID {review.id}")
            return ReviewReplyResponse(
                reply="Thanks for your feedback!",
                tags=[]
            )
        except Exception as e:
            logger.error(f"Failed to generate reply for review ID {review.id}", exc_info=e)
            raise HTTPException(status_code=500, detail="Failed to generate reply")
 