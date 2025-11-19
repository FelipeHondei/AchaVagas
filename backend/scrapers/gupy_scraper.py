from __future__ import annotations

import logging
from typing import Iterable

import requests

from .base_scraper import BaseScraper

log = logging.getLogger(__name__)


class GupyScraper(BaseScraper):
    source = "gupy"
    BASE_URL = "https://portal.api.gupy.io/api/job-search"

    def fetch_jobs(self, query: str, location: str) -> Iterable[dict]:
        payload = {
            "query": query,
            "location": location,
            "remote": None,
            "published": True,
            "limit": 30,
        }
        response = requests.post(self.BASE_URL, json=payload, timeout=20)
        if response.status_code != 200:
            log.warning("Gupy returned %s", response.status_code)
            return []

        data = response.json()
        for job in data.get("data", []):
            yield self.normalize_job(
                {
                    "external_id": job.get("id"),
                    "title": job.get("name"),
                    "company": job.get("career", {}).get("name"),
                    "location": job.get("workplaceType"),
                    "url": job.get("career", {}).get("websiteUrl"),
                    "description": job.get("description"),
                }
            )

