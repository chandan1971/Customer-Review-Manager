from fastapi import FastAPI
from app.config import settings
from app.routes import analytics_routes, health_routes,review_routes

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    docs_url=settings.DOCS_URL,  
    redoc_url=settings.REDOCS_URL 
)


app.include_router(health_routes.router, prefix="/health", tags=["Health"])
app.include_router(review_routes.router, prefix="/reviews", tags=["Reviews"])
app.include_router(analytics_routes.router, prefix="/analytics", tags=["Analytics"])

