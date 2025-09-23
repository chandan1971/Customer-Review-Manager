from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.connections.postgres_db import get_db
from app.controllers.analytics_controller import AnalyticsController  # new controller

router = APIRouter()


@router.get("/", summary="Analytics by topic and sentiment", description="Returns count of reviews per topic and sentiment for charting.")
def analytics(db: Session = Depends(get_db)):
    controller = AnalyticsController(db)
    return controller.get_analytics()
