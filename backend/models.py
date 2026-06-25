from sqlalchemy import Column, Integer, String, Boolean
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

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, index=True)
    reviewer_name = Column(String)
    rating = Column(Integer)
    comment = Column(String)
