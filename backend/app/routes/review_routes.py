from fastapi import APIRouter,Depends
from app.schemas.review_DTO import ReviewCreateDTO
from app.controllers.review_controller import ReviewController
from sqlalchemy.orm import Session
from app.connections.postgres_db import get_db

router = APIRouter()

@router.post("/ingest", summary="Add Review", description="Add review and persist.")
def ingest_review(review : list[ReviewCreateDTO], db: Session = Depends(get_db)):
    controller = ReviewController(db)
    return controller.ingest_review(review) 