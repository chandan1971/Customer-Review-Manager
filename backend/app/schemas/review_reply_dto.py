from pydantic import BaseModel
from typing import List

class ReviewReplyResponse(BaseModel):
    reply: str
    tags: List[str]
