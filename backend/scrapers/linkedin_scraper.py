from __future__ import annotations

import logging
from typing import Iterable

import requests
from bs4 import BeautifulSoup

from backend.config import get_settings
from .base_scraper import BaseScraper


log = logging.getLogger(__name__)
settings = get_settings()


class LinkedInScraper(BaseScraper):
    source = "linkedin"
    BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

    def fetch_jobs(self, query: str, location: str) -> Iterable[dict]:
        params = {"keywords": query, "location": location, "start": 0}
        while True:
            response = requests.get(self.BASE_URL, params=params, timeout=20)
            if response.status_code != 200:
                log.warning("LinkedIn returned %s", response.status_code)
                break

            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select("li")
            if not cards:
                break

            for card in cards:
                yield self.normalize_job(
                    {
                        "title": card.find("h3").get_text(strip=True) if card.find("h3") else "",
                        "company": card.find("h4").get_text(strip=True) if card.find("h4") else "",
                        "location": card.find("span", class_="job-search-card__location").get_text(strip=True)
                        if card.find("span", class_="job-search-card__location")
                        else settings.scraping_default_location,
                        "url": card.find("a")["href"] if card.find("a") else "",
                        "description": card.get_text(strip=True),
                    }
                )

            params["start"] += len(cards)

