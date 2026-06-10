from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WorkerCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    bio: Optional[str] = None
    municipality: str
    categories: str
    whatsapp: Optional[str] = None
    photo_url: Optional[str] = None

class WorkerResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    bio: Optional[str] = None
    municipality: str
    categories: str
    whatsapp: Optional[str] = None
    photo_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    trial_ends_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    worker_id: int
    reviewer_name: str
    rating: int
    comment: Optional[str] = None

class ReviewResponse(BaseModel):
    id: int
    worker_id: int
    reviewer_name: str
    rating: int
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
