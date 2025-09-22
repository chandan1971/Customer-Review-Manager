# app/schemas/review_dto.py
from pydantic import BaseModel
from datetime import date

class ReviewDAO(BaseModel):
    id: int
    location: str
    rating: int
    text: str
    date: date 

