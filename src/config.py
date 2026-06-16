"""Application configuration loaded from environment variables."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Settings needed to call the WHO ICD-11 API."""

    client_id: str
    client_secret: str
    token_url: str
    base_url: str


def get_settings() -> Settings:
    """Return application settings from environment variables."""
    return Settings(
        client_id=os.getenv("ICD_CLIENT_ID", ""),
        client_secret=os.getenv("ICD_CLIENT_SECRET", ""),
        token_url=os.getenv(
            "ICD_TOKEN_URL",
            "https://icdaccessmanagement.who.int/connect/token",
        ),
        base_url=os.getenv(
            "ICD_BASE_URL",
            "https://id.who.int/icd/release/11/2026-01/mms",
        ),
    )
