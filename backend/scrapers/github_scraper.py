from __future__ import annotations

import logging
from typing import Iterable

import requests

from .base_scraper import BaseScraper

log = logging.getLogger(__name__)


class GitHubJobsScraper(BaseScraper):
    source = "github"
    BASE_URL = "https://jobs.github.com/positions.json"

    def fetch_jobs(self, query: str, location: str) -> Iterable[dict]:
        params = {"description": query, "location": location}
        response = requests.get(self.BASE_URL, params=params, timeout=20)
        if response.status_code != 200:
            log.warning("GitHub Jobs returned %s", response.status_code)
            return []

        for job in response.json():
            yield self.normalize_job(
                {
                    "external_id": job.get("id"),
                    "title": job.get("title"),
                    "company": job.get("company"),
                    "location": job.get("location"),
                    "url": job.get("url"),
                    "description": job.get("description"),
                }
            )

