from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text, Float, Boolean
from sqlalchemy.dialects.postgresql import JSONB

from backend.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), nullable=False)
    external_id = Column(String(255), nullable=True, index=True, unique=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    url = Column(String(500), nullable=False)

    description = Column(Text, nullable=True)
    skills = Column(JSONB, nullable=True)
    salary = Column(String(120), nullable=True)
    seniority = Column(String(120), nullable=True)
    employment_type = Column(String(120), nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    match_score = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

