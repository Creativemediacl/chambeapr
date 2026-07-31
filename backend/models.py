from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from database import Base

class Worker(Base):
    __tablename__ = "workers"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    profession = Column(String, index=True)
    municipality = Column(String, index=True)
    description = Column(String)
    phone_number = Column(String)
    whatsapp_number = Column(String)
    email = Column(String, unique=True, index=True)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    license_photo = Column(String, nullable=True)
    license_number = Column(String, nullable=True)
    stripe_customer_id = Column(String, nullable=True)
    subscription_status = Column(String, default="trial")
    trial_ends_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=30))
    accepted_terms = Column(Boolean, default=False)
    hashed_password = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, index=True)
    reviewer_name = Column(String)
    rating = Column(Integer)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
