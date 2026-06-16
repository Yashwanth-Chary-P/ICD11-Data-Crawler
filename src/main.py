"""Command-line entry point for the ICD-11 crawler."""

import argparse
import logging

import requests

from auth import TokenManager
from config import get_settings
from crawler import Crawler
from exporter import open_csv_writer
from icd_client import ICDClient


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Crawl WHO ICD-11 data into CSV.")
    parser.add_argument(
        "--chapter-id",
        required=True,
        help="ICD-11 chapter/entity ID to start crawling from.",
    )
    parser.add_argument(
        "--output",
        default="data/outputs/tm2.csv",
        help="Output CSV path.",
    )
    return parser.parse_args()


def setup_logging() -> None:
    """Configure basic application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def main() -> None:
    """Run the crawler from the command line."""
    setup_logging()
    args = parse_args()
    settings = get_settings()

    if not settings.client_id or not settings.client_secret:
        raise RuntimeError(
            "Missing WHO ICD API credentials. Set ICD_CLIENT_ID and "
            "ICD_CLIENT_SECRET in your .env file."
        )

    with requests.Session() as session:
        token_manager = TokenManager(session, settings)
        token_manager.refresh_token()

        client = ICDClient(session, settings, token_manager)
        crawler = Crawler(client)

        csv_file, writer = open_csv_writer(args.output)
        with csv_file:
            crawler.run_chapter(str(args.chapter_id), writer, csv_file)

    logging.getLogger(__name__).info("DONE: %s", args.output)


if __name__ == "__main__":
    main()
