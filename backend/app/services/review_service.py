from sqlalchemy.orm import Session
from app.schemas.review_dao import ReviewDAO
from app.schemas.review_DTO import ReviewCreateDTO
from app.utils.db_utils import insert_reviews_bulk
from app.utils.logger import get_logger
from app.utils.db_utils import dao_to_dto
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
