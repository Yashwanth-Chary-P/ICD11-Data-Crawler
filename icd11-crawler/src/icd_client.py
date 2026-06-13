"""HTTP client for WHO ICD-11 entities."""

import logging
import time
from typing import Any, Optional

import requests

from auth import TokenManager
from config import Settings


logger = logging.getLogger(__name__)


class ICDClient:
    """Client for fetching normal and residual ICD-11 entities."""

    def __init__(
        self,
        session: requests.Session,
        settings: Settings,
        token_manager: TokenManager,
    ) -> None:
        self.session = session
        self.settings = settings
        self.token_manager = token_manager

    def get_entity(self, entity_id: str, residual: Optional[str] = None) -> Optional[dict[str, Any]]:
        """Fetch an ICD entity, retrying and refreshing the token on 401 responses."""
        if residual:
            url = f"{self.settings.base_url}/{entity_id}/{residual}"
        else:
            url = f"{self.settings.base_url}/{entity_id}"

        for _ in range(5):
            try:
                headers = {
                    "Authorization": f"Bearer {self.token_manager.token}",
                    "API-Version": "v2",
                    "Accept-Language": "en",
                }

                response = self.session.get(url, headers=headers, timeout=10)

                if response.status_code == 401:
                    logger.warning("Token expired. Refreshing...")
                    self.token_manager.refresh_token()
                    continue

                if response.status_code == 200:
                    return response.json()

            except Exception as exc:
                logger.debug("Failed to fetch entity %s: %s", entity_id, exc)
                time.sleep(1)

        return None
