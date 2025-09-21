from fastapi import APIRouter
from app.services.health_service import HealthService

router = APIRouter()
healthService = HealthService()

@router.get("/", summary="Health Check", description="Check if service is healthy")
def health_check():
    return healthService.get_status()