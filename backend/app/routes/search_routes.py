from fastapi import APIRouter,Query,Depends
from sqlalchemy.orm import Session
from app.connections.postgres_db import get_db
from app.controllers.search_controller import SearchController

router = APIRouter()

@router.get("/", summary="Search Review", description="Search top similar reviews")
def search(
    q: str = Query(..., min_length=1),
    k: int = Query(5, ge=1, le=20),  
    db: Session = Depends(get_db)
):
    controller = SearchController(db)
    return controller.search_reviews(q, k)