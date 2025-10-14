# app/schemas/review_dto.py
from pydantic import BaseModel
from datetime import date

class ReviewDAO(BaseModel):
    location: str
    rating: int
    text: str
    date: date 

