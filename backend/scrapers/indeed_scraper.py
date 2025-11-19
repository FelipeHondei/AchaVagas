from __future__ import annotations

import logging
from typing import Iterable

import requests
from bs4 import BeautifulSoup

from .base_scraper import BaseScraper

log = logging.getLogger(__name__)


class IndeedScraper(BaseScraper):
    source = "indeed"
    BASE_URL = "https://www.indeed.com/jobs"

    def fetch_jobs(self, query: str, location: str) -> Iterable[dict]:
        params = {"q": query, "l": location}
        response = requests.get(self.BASE_URL, params=params, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            log.warning("Indeed returned %s", response.status_code)
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        for card in soup.select("div.job_seen_beacon"):
            title_el = card.select_one("h2 a")
            company = card.select_one(".companyName")
            location_el = card.select_one(".companyLocation")
            summary = card.select_one(".job-snippet")

            yield self.normalize_job(
                {
                    "title": title_el.get_text(strip=True) if title_el else "",
                    "company": company.get_text(strip=True) if company else "",
                    "location": location_el.get_text(strip=True) if location_el else "",
                    "url": f"https://www.indeed.com{title_el['href']}" if title_el and title_el.has_attr("href") else "",
                    "description": summary.get_text("\n", strip=True) if summary else "",
                }
            )

