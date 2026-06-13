"""CSV export helpers."""

import csv
from pathlib import Path
from typing import TextIO

from extractor import CSV_FIELDNAMES


def open_csv_writer(output_path: str) -> tuple[TextIO, csv.DictWriter]:
    """Open a CSV file and return the file handle and configured DictWriter."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    csv_file = path.open("w", newline="", encoding="utf-8")
    writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDNAMES)
    writer.writeheader()

    return csv_file, writer
