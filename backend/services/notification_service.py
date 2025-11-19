from __future__ import annotations

import logging
from emails import Message
from emails.smtp import SMTPResponse

from backend.config import get_settings


log = logging.getLogger(__name__)
settings = get_settings()


class NotificationService:
    def __init__(self):
        self.sender = settings.email_from

    def send_digest(self, recipient: str, jobs: list[dict]) -> SMTPResponse | None:
        if not settings.email_host:
            log.warning("Email host not configured. Skipping digest.")
            return None

        body = self._render_body(jobs)
        message = Message(
            subject="Resumo diário de vagas",
            mail_from=self.sender,
            html=body,
        )

        response = message.send(
            smtp={
                "host": settings.email_host,
                "port": settings.email_port,
                "user": settings.email_user,
                "password": settings.email_password,
                "tls": True,
            },
            to=recipient,
        )
        return response

    def _render_body(self, jobs: list[dict]) -> str:
        items = "".join(
            f"<li><strong>{job['title']}</strong> @ {job['company']} ({job.get('match_score', 0):.0%}) "
            f"- <a href='{job['url']}'>abrir</a></li>"
            for job in jobs
        )
        return f"<h3>Top vagas do dia</h3><ol>{items}</ol>"

