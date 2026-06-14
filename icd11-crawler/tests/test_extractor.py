import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from extractor import extract, safe_join


def test_safe_join_joins_label_values() -> None:
    items = [
        {"label": {"@value": "First"}},
        {"label": {"@value": "Second"}},
    ]

    assert safe_join(items) == "First; Second"


def test_safe_join_skips_items_without_label() -> None:
    items = [
        {"label": {"@value": "First"}},
        {"not_label": {"@value": "Ignored"}},
    ]

    assert safe_join(items) == "First"


def test_extract_returns_none_without_code() -> None:
    assert extract({"title": {"@value": "No code"}}) is None


def test_extract_preserves_output_fields() -> None:
    data = {
        "code": "AB12",
        "title": {"@value": "Title"},
        "fullySpecifiedName": {"@value": "Full Name"},
        "definition": {"@value": "Description"},
        "inclusion": [{"label": {"@value": "Inclusion"}}],
        "exclusion": [{"label": {"@value": "Exclusion"}}],
        "indexTerm": [{"label": {"@value": "Index"}}],
    }

    assert extract(data) == {
        "Code": "AB12",
        "title": "Title",
        "Fully Specified Name": "Full Name",
        "Description": "Description",
        "Inclusions": "Inclusion",
        "Exclusions": "Exclusion",
        "Index Terms": "Index",
    }
