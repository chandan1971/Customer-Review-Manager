from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ReviewModel(Base):
    __tablename__ = "reviews"  
    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(String, nullable=False)
    review_date = Column(Date, nullable=False)
