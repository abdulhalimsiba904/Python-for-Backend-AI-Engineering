"""Real files in pytest-owned temporary directories, never project samples."""
import json

import pytest

from data_toolkit.models import DocumentRecord
from data_toolkit.processing import load_transactions, process_document
from data_toolkit.readers import read_json
from data_toolkit.reports import calculate_average, count_categories


@pytest.mark.parametrize("suffix", ["json", "csv"])
def test_loading_through_reporting(tmp_path, transactions, suffix):
    path = tmp_path / f"input.{suffix}"
    if suffix == "json":
        path.write_text(json.dumps(transactions), encoding="utf-8")
    else:
        path.write_text("id,amount,category\n T1 ,2, Food \nT2,4,FOOD\nT2,6,Transport\n",
                        encoding="utf-8")
    record = DocumentRecord("DOC-8", path.name, suffix)
    rows = process_document(record, path)
    assert calculate_average([row["amount"] for row in rows]) == 4
    assert count_categories(rows) == {"food": 2, "transport": 1}
    assert record.processing_status == "completed"


@pytest.mark.parametrize("contents, error, message", [
    ("[{]", json.JSONDecodeError, None),
    ("", json.JSONDecodeError, None),
    ('{}', ValueError, "must be a list"),
    ('[null]', ValueError, "dictionary"),
])
def test_invalid_json_boundary(tmp_path, contents, error, message):
    path = tmp_path / "invalid.json"
    path.write_text(contents, encoding="utf-8")
    with pytest.raises(error, match=message):
        read_json(path)


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_transactions(tmp_path / "missing.json")


def test_missing_csv_field_is_rejected(tmp_path):
    path = tmp_path / "missing.csv"
    path.write_text("id,amount\nT1,2\n", encoding="utf-8")
    with pytest.raises(ValueError, match="category"):
        load_transactions(path)


def test_empty_json_list_completes(tmp_path):
    path = tmp_path / "empty.json"
    path.write_text("[]", encoding="utf-8")
    assert load_transactions(path) == []


def test_regression_malformed_json_marks_record_failed(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("[{]", encoding="utf-8")
    record = DocumentRecord("DOC-8", path.name, "json")
    with pytest.raises(json.JSONDecodeError):
        process_document(record, path)
    assert record.processing_status == "failed"
    assert record.validation_errors == [
        "Invalid JSON syntax. Check commas and quotes."
    ]
