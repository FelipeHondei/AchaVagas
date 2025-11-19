from __future__ import annotations

from sqlalchemy.orm import Session

from backend.models import Job, UserProfile
from .nlp_service import NLPService


class MatchingService:
    def __init__(self, db: Session):
        self.db = db
        self.nlp = NLPService()

    def compute_scores(self, profile: UserProfile, jobs: list[Job]) -> list[tuple[Job, float]]:
        profile_text = self._profile_to_text(profile)
        job_texts = [self._job_to_text(job) for job in jobs]
        scores = self.nlp.similarity(profile_text, job_texts)

        ranked = []
        for job, score in zip(jobs, scores, strict=False):
            job.match_score = float(score)
            ranked.append((job, float(score)))
        return sorted(ranked, key=lambda item: item[1], reverse=True)

    def _profile_to_text(self, profile: UserProfile) -> str:
        parts = [
            profile.headline or "",
            " ".join(profile.desired_roles or []),
            " ".join(profile.skills or []),
            profile.summary or "",
        ]
        return " ".join(filter(None, parts))

    def _job_to_text(self, job: Job) -> str:
        parts = [
            job.title or "",
            job.company or "",
            job.description or "",
            " ".join(job.skills or []),
        ]
        return " ".join(filter(None, parts))

