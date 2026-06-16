"""Depth-first ICD-11 crawler."""

import csv
import logging
import time
from typing import TextIO

from extractor import extract
from icd_client import ICDClient


logger = logging.getLogger(__name__)


class Crawler:
    """Traverse ICD-11 entities and write extracted rows to CSV."""

    def __init__(self, client: ICDClient) -> None:
        self.client = client
        self.visited: set[str] = set()

    def dfs(self, entity_id: str, writer: csv.DictWriter, csv_file: TextIO) -> None:
        """Traverse an ICD entity and its children using DFS."""
        if entity_id in self.visited:
            return

        self.visited.add(entity_id)

        data = self.client.get_entity(entity_id)
        if data:
            row = extract(data)

            if row:
                writer.writerow(row)
                csv_file.flush()
                logger.info("Saved: %s", row["Code"])

            for residual in ["other", "unspecified"]:
                residual_data = self.client.get_entity(entity_id, residual)

                if residual_data:
                    residual_row = extract(residual_data)

                    if residual_row:
                        writer.writerow(residual_row)
                        csv_file.flush()
                        logger.info("Saved residual: %s", residual_row["Code"])

            for child in data.get("child", []):
                child_id = child.split("/")[-1]
                self.dfs(child_id, writer, csv_file)

        time.sleep(0.05)

    def run_chapter(self, chapter_id: str, writer: csv.DictWriter, csv_file: TextIO) -> None:
        """Start a fresh traversal for one ICD chapter."""
        self.visited = set()
        self.dfs(chapter_id, writer, csv_file)
