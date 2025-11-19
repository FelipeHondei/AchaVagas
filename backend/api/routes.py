from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from backend.config import get_settings
from backend.database import get_db
from backend.models import Job, UserProfile
from backend.schemas import JobSchema, UserProfileCreate, UserProfileSchema
from backend.tasks.celery_tasks import fetch_latest_jobs, run_matching_and_notify


settings = get_settings()
app = FastAPI(title=settings.app_name)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/jobs", response_model=list[JobSchema])
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).order_by(Job.created_at.desc()).limit(50).all()
    return jobs


@app.get("/profiles/{profile_id}", response_model=UserProfileSchema)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).get(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@app.post("/profiles", response_model=UserProfileSchema)
def create_profile(profile: UserProfileCreate, db: Session = Depends(get_db)):
    profile_model = UserProfile(**profile.dict())
    db.add(profile_model)
    db.commit()
    db.refresh(profile_model)
    return profile_model


@app.post("/jobs/refresh")
def trigger_scraping(query: str | None = None, location: str | None = None):
    fetch_latest_jobs.delay(query, location)
    return {"detail": "Scraping started"}


@app.post("/matches/{profile_id}/run")
def trigger_match(profile_id: int):
    run_matching_and_notify.delay(profile_id)
    return {"detail": "Matching started"}

