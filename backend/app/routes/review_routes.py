from fastapi import APIRouter,Depends
from app.schemas.review_dao import ReviewDAO
from app.controllers.review_controller import ReviewController
from sqlalchemy.orm import Session
from app.connections.postgres_db import get_db

router = APIRouter()

@router.post("/ingest", summary="Add Review", description="Add review and persist.")
def ingest_review(reviews : list[ReviewDAO], db: Session = Depends(get_db)):
    controller = ReviewController(db)
    return controller.ingest_review(reviews) 

@router.get("/{id}",summary="Get Review by ID",description="Fetch a single review record by its ID.")
def get_review(id: int, db: Session = Depends(get_db)):
    controller = ReviewController(db)
    return controller.get_review_by_id(id)