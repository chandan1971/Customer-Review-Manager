from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.search_service import SearchService

class SearchController :
    def __init__(self, db: Session):
        self.service = SearchService(db)

    def search_reviews(self, query: str, top_k: int = 5):
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        return self.service.search_reviews(query, top_k)