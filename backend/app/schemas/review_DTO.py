# app/schemas/review_dto.py
from pydantic import BaseModel
from datetime import datetime

class ReviewCreateDTO(BaseModel):
    id: int
    location: str
    rating: int
    text: str
    review_date: datetime 

