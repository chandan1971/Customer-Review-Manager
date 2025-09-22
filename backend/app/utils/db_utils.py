from sqlalchemy.orm import Session
from app.schemas.review_DTO import ReviewCreateDTO
from sqlalchemy import text
from typing import List
from app.constants.db_constants import REVIEWS_TABLE
from app.utils.logger import get_logger
from pydantic import BaseModel

logger = get_logger(__name__)

def build_insert_query(table_name: str, dto:BaseModel):
    data = dto.model_dump()
    columns = ", ".join(data.keys())
    placeholders = ", ".join([f":{key}" for key in data.keys()])

    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    return query, data

def insert_reviews(db: Session, review: ReviewCreateDTO) -> int:
    rows_inserted = 0
    query, params = build_insert_query(REVIEWS_TABLE, review)
    try:
        db.execute(text(query), params)
        rows_inserted += 1
        db.commit() 
    except Exception as e:
        db.rollback()
        logger.info("DB Exception while inserting review",e)
        
            
    return rows_inserted