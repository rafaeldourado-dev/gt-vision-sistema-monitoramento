# backend/api/schemas.py

from pydantic import BaseModel
from datetime import datetime

class AlertSchema(BaseModel):
    id: int
    title: str
    description: str
    timestamp: datetime
    is_critical: bool
    image_path: str | None = None
    video_path: str | None = None

    class Config:
        from_attributes = True