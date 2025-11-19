from abc import ABC, abstractmethod
from typing import Iterable


class BaseScraper(ABC):
    source: str

    def __init__(self, session=None):
        self.session = session

    @abstractmethod
    def fetch_jobs(self, query: str, location: str) -> Iterable[dict]:
        """Return an iterable of job dictionaries."""

    def normalize_job(self, job: dict) -> dict:
        defaults = {"source": self.source}
        defaults.update(job)
        return defaults

