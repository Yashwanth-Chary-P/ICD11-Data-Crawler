"""Authentication helpers for the WHO ICD-11 API."""

import logging
from typing import Optional

import requests

from config import Settings


logger = logging.getLogger(__name__)


class TokenManager:
    """Fetches and stores the current ICD API access token."""

    def __init__(self, session: requests.Session, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.token: Optional[str] = None

    def refresh_token(self) -> str:
        """Request a new access token and store it."""
        data = {
            "client_id": self.settings.client_id,
            "client_secret": self.settings.client_secret,
            "scope": "icdapi_access",
            "grant_type": "client_credentials",
        }

        response = self.session.post(self.settings.token_url, data=data, timeout=10)
        response.raise_for_status()

        token = response.json().get("access_token")
        if not token:
            raise RuntimeError("WHO ICD API token response did not include access_token.")

        self.token = token
        logger.info("Token refreshed")
        return token
