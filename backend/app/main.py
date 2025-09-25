from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import analytics_routes, health_routes,review_routes,search_routes

origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173",
    "https://peaceful-pudding-7ab335.netlify.app"
]

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    docs_url=settings.DOCS_URL,  
    redoc_url=settings.REDOCS_URL 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],     
    allow_headers=["*"],     
)


app.include_router(health_routes.router, prefix="/health", tags=["Health"])
app.include_router(review_routes.router, prefix="/reviews", tags=["Reviews"])
app.include_router(analytics_routes.router, prefix="/analytics", tags=["Analytics"])
app.include_router(search_routes.router, prefix="/search", tags=["Search"])
