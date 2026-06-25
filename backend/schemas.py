from pydantic import BaseModel
from typing import Optional

class WorkerCreate(BaseModel):
    full_name: str
    profession: str
    municipality: str
    description: str
    phone_number: str
    whatsapp_number: str
    email: str

class WorkerPublic(BaseModel):
    id: int
    full_name: str
    profession: str
    municipality: str
    description: str
    is_verified: bool
    is_active: bool

    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    worker_id: int
    reviewer_name: str
    rating: int
    comment: Optional[str] = None

class ReviewPublic(BaseModel):
    id: int
    worker_id: int
    reviewer_name: str
    rating: int
    comment: Optional[str] = None

    class Config:
        from_attributes = True
