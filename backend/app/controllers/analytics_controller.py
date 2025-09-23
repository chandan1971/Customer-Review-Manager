from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services.analytics_service import AnalyticsService

class AnalyticsController:
    def __init__(self, db: Session):
        self.service = AnalyticsService(db)

    def get_analytics(self):
        try:
            analytics = self.service.get_analytics()
            return {"analytics": analytics}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
