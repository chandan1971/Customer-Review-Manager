from pydantic import BaseModel, Field
from typing import Optional

class ReviewFilterRequest(BaseModel):
    location: Optional[str] = Field(None, description="Filter by location")
    sentiment: Optional[str] = Field(None, description="Filter by sentiment")
    q: Optional[str] = Field(None, description="Search query")
    page: int = Field(1, ge=1, description="Page number, starting from 1")
    page_size: int = Field(10, ge=1, le=100, description="Number of reviews per page")
