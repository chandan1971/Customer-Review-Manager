# app/schemas/review_dto.py
from pydantic import BaseModel
from datetime import date

class ReviewCreateDTO(BaseModel):
    id: int
    location: str
    rating: int
    review_text: str
    review_date: date 
    sentiment: str | None = None
    topics: str | None = None

