from __future__ import annotations

import logging
from datetime import datetime

from celery import Celery
from sqlalchemy.orm import Session

from backend.config import get_settings
from backend.database import SessionLocal
from backend.models import Job, UserProfile
from backend.scrapers.github_scraper import GitHubJobsScraper
from backend.scrapers.gupy_scraper import GupyScraper
from backend.scrapers.indeed_scraper import IndeedScraper
from backend.scrapers.linkedin_scraper import LinkedInScraper
from backend.services.matching_service import MatchingService
from backend.services.notification_service import NotificationService


settings = get_settings()
celery_app = Celery("job_aggregator", broker=settings.celery_broker_url, backend=settings.celery_result_backend)

log = logging.getLogger(__name__)


def _scrapers():
    return [
        LinkedInScraper(),
        IndeedScraper(),
        GitHubJobsScraper(),
        GupyScraper(),
    ]


@celery_app.task
def fetch_latest_jobs(query: str | None = None, location: str | None = None):
    query = query or settings.scraping_default_query
    location = location or settings.scraping_default_location

    with SessionLocal() as db:
        for scraper in _scrapers():
            for job_data in scraper.fetch_jobs(query, location):
                upsert_job(db, job_data)
        db.commit()


def upsert_job(db: Session, job_data: dict):
    existing = None
    external_id = job_data.get("external_id")
    if external_id:
        existing = db.query(Job).filter(Job.external_id == external_id).one_or_none()

    if existing:
        for key, value in job_data.items():
            setattr(existing, key, value)
        existing.updated_at = datetime.utcnow()
    else:
        db.add(Job(**job_data))


@celery_app.task
def run_matching_and_notify(profile_id: int):
    with SessionLocal() as db:
        profile = db.query(UserProfile).get(profile_id)
        if not profile:
            log.warning("Profile %s not found", profile_id)
            return

        jobs = db.query(Job).filter(Job.is_active.is_(True)).all()
        matching = MatchingService(db)
        ranked = matching.compute_scores(profile, jobs)

        best_jobs = [job for job, _ in ranked[:10]]
        notification = NotificationService()
        notification.send_digest(profile.email, [job.__dict__ for job in best_jobs])

        db.commit()

