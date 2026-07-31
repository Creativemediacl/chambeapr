from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    email: str
    password: str
from datetime import datetime

class WorkerCreate(BaseModel):
    full_name: str
    profession: str
    municipality: str
    description: str
    phone_number: str
    whatsapp_number: str
    email: str
    accepted_terms: bool
    password: str

class WorkerPublic(BaseModel):
    id: int
    full_name: str
    profession: str
    municipality: str
    description: str
    is_verified: bool
    is_active: bool
    license_number: Optional[str] = None
    subscription_status: str = "trial"
    trial_ends_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

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
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ForgotPasswordRequest(BaseModel):
    email: str
