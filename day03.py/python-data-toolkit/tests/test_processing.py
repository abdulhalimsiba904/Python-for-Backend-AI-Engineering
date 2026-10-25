"""Check composition of document state with the existing transaction functions."""
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from data_toolkit.models import DocumentRecord
from data_toolkit.processing import load_transactions, process_document
from data_toolkit.reports import calculate_average

ROOT = Path(__file__).resolve().parents[1]


def test_json_and_csv_processing_preserves_reports() -> None:
    for suffix in ("json", "csv"):
        path = ROOT / "samples" / f"transactions.{suffix}"
        record = DocumentRecord(f"DOC-{suffix}", path.name, suffix)
        rows = process_document(record, path)
        assert rows == load_transactions(path)
        assert len(rows) == 3
        assert calculate_average([row["amount"] for row in rows]) == 75.0
        assert record.processing_status == "completed"
        assert record.validation_errors == []


def test_processing_preserves_extra_fields_and_refunds() -> None:
    with TemporaryDirectory() as folder:
        path = Path(folder) / "input.json"
        path.write_text(json.dumps([
            {"id": " T1 ", "amount": "-5", "category": " Food ", "note": "kept"}
        ]), encoding="utf-8")
        record = DocumentRecord("DOC-001", path.name, "json")
        assert process_document(record, path) == [
            {"id": "T1", "amount": -5.0, "category": "food", "note": "kept"}
        ]
        assert record.processing_status == "completed"


def test_empty_dataset_completes() -> None:
    with TemporaryDirectory() as folder:
        path = Path(folder) / "input.json"
        path.write_text("[]", encoding="utf-8")
        record = DocumentRecord("DOC-001", path.name, "json")
        assert process_document(record, path) == []
        assert record.processing_status == "completed"


def test_missing_file_records_failure_and_reraises() -> None:
    with TemporaryDirectory() as folder:
        path = Path(folder) / "missing.json"
        record = DocumentRecord("DOC-001", path.name, "json")
        try:
            process_document(record, path)
        except FileNotFoundError:
            pass
        else:
            raise AssertionError("Expected the original missing-file exception")
        assert record.processing_status == "failed"
        assert record.validation_errors == [
            "Could not read document (FileNotFoundError). Check file access."
        ]
        assert str(path) not in record.validation_errors[0]


def test_malformed_json_records_safe_failure() -> None:
    path = ROOT / "samples" / "malformed.json"
    record = DocumentRecord("DOC-001", path.name, "json")
    try:
        process_document(record, path)
    except json.JSONDecodeError:
        pass
    else:
        raise AssertionError("Expected the original JSON error")
    assert record.processing_status == "failed"
    assert record.validation_errors == ["Invalid JSON syntax. Check commas and quotes."]


def test_invalid_transaction_does_not_echo_contents() -> None:
    with TemporaryDirectory() as folder:
        path = Path(folder) / "input.json"
        for amount in (True, "PRIVATE-TOKEN", "nan"):
            path.write_text(json.dumps([
                {"id": "PRIVATE-ID", "amount": amount, "category": "food"}
            ]), encoding="utf-8")
            record = DocumentRecord("DOC-001", path.name, "json")
            try:
                process_document(record, path)
            except ValueError:
                pass
            else:
                raise AssertionError("Expected invalid transaction rejection")
            assert record.processing_status == "failed"
            assert record.validation_errors == [
                "Invalid document data. Check the format and required transaction fields."
            ]
            assert "PRIVATE" not in record.get_summary() + str(record.validation_errors)


def test_metadata_must_match_input_file() -> None:
    path = ROOT / "samples" / "transactions.json"
    for filename, document_type in (("different.json", "json"), (path.name, "csv")):
        record = DocumentRecord("DOC-001", filename, document_type)
        try:
            process_document(record, path)
        except ValueError as error:
            assert "metadata" in str(error)
        else:
            raise AssertionError("Accepted mismatched metadata")
        assert record.processing_status == "failed"


def test_metadata_only_types_do_not_add_readers() -> None:
    for suffix in ("pdf", "txt"):
        record = DocumentRecord("DOC-001", f"input.{suffix}", suffix)
        try:
            process_document(record, ROOT / f"input.{suffix}")
        except ValueError as error:
            assert "Unsupported file format" in str(error)
        else:
            raise AssertionError("Unexpected transaction reader")
        assert record.processing_status == "failed"


def test_failed_attempt_cannot_be_silently_retried() -> None:
    path = ROOT / "samples" / "transactions.json"
    record = DocumentRecord("DOC-001", path.name, "json")
    record.mark_failed("An earlier attempt failed.")
    try:
        process_document(record, path)
    except ValueError:
        pass
    else:
        raise AssertionError("Unexpected retry of a failed record")
    assert record.validation_errors == ["An earlier attempt failed."]


def test_cli_stdout_remains_unchanged() -> None:
    environment = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    for suffix in ("json", "csv"):
        relative_path = f"samples/transactions.{suffix}"
        result = subprocess.run(
            [sys.executable, "-m", "data_toolkit.cli", relative_path],
            cwd=ROOT, env=environment, capture_output=True, text=True,
        )
        assert result.returncode == 0, result.stderr
        assert result.stderr == ""
        assert result.stdout == (
            "=== Python Data Toolkit ===\n"
            f"Input file: {relative_path}\n"
            "Transaction count: 3\n"
            "Average amount: 75.0\n"
            "Category counts: {'food': 2, 'transport': 1}\n"
            "Duplicate IDs: set()\n"
        )


def test_demo_runs_without_pythonpath() -> None:
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    result = subprocess.run(
        [sys.executable, str(ROOT / "document_record_demo.py")],
        cwd=ROOT.parent, env=environment, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert "Status after mark_processing(): processing" in result.stdout
    assert "completed | errors: 0" in result.stdout
    assert "failed | errors: 1" in result.stdout
    assert "Average amount: 75.0" in result.stdout
