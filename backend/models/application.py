from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from backend.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)

    score = Column(Numeric(5, 2), nullable=True)
    status = Column(String(50), default="pending")

    created_at = Column(DateTime, default=datetime.utcnow)
    notified_at = Column(DateTime, nullable=True)

    job = relationship("Job", backref="applications")
    profile = relationship("UserProfile", backref="applications")

