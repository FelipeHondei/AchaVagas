from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr


class JobSchema(BaseModel):
    id: int
    title: str
    company: str
    location: Optional[str] = None
    url: str
    description: Optional[str] = None
    match_score: Optional[float] = None
    source: str
    scraped_at: datetime

    class Config:
        from_attributes = True


class UserProfileBase(BaseModel):
    name: str
    email: EmailStr
    headline: Optional[str] = None
    desired_roles: List[str] = Field(default_factory=list)
    locations: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    summary: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileSchema(UserProfileBase):
    id: int

    class Config:
        from_attributes = True

