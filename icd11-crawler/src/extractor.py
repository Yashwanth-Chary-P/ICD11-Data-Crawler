"""Extract CSV rows from ICD-11 API responses."""

from typing import Any, Optional


CSV_FIELDNAMES = [
    "Code",
    "title",
    "Fully Specified Name",
    "Description",
    "Inclusions",
    "Exclusions",
    "Index Terms",
]


def safe_join(items: list[dict[str, Any]]) -> str:
    """Join ICD label values with semicolons."""
    return "; ".join(
        [
            item.get("label", {}).get("@value", "")
            for item in items
            if item.get("label")
        ]
    )


def extract(data: dict[str, Any]) -> Optional[dict[str, str]]:
    """Extract a CSV row from an ICD entity response."""
    code = data.get("code", "")
    if not code:
        return None

    return {
        "Code": code,
        "title": data.get("title", {}).get("@value", ""),
        "Fully Specified Name": data.get("fullySpecifiedName", {}).get("@value", ""),
        "Description": data.get("definition", {}).get("@value", ""),
        "Inclusions": safe_join(data.get("inclusion", [])),
        "Exclusions": safe_join(data.get("exclusion", [])),
        "Index Terms": safe_join(data.get("indexTerm", [])),
    }
