"""Compose document state with function-based reading and normalization."""
import csv
import json
from pathlib import Path

from data_toolkit.models import DocumentRecord
from data_toolkit.readers import read_csv, read_json
from data_toolkit.transformers import normalize_transactions


def load_transactions(file_path: str | Path) -> list[dict]:
    """Load transactions from a supported file and normalize their data."""
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".json":
        transactions = read_json(path)
    elif suffix == ".csv":
        transactions = read_csv(path)
    else:
        raise ValueError("Unsupported file format. Use a .json or .csv file.")

    return normalize_transactions(transactions)


def process_document(record: DocumentRecord, file_path: str | Path) -> list[dict]:
    """Read and validate JSON/CSV transactions, updating one pending record.

    Expected input errors mark the record failed and are re-raised unchanged.
    Stored errors omit input contents and paths. Unexpected programming errors
    propagate instead of being disguised as ordinary validation failures.
    Completed means loading and normalization finished; reporting is separate.
    """
    path = Path(file_path)
    record.mark_processing()
    try:
        if record.filename != path.name or record.document_type != path.suffix[1:].lower():
            raise ValueError("Document metadata must match the input filename and type.")
        transactions = load_transactions(path)
    except json.JSONDecodeError:
        record.mark_failed("Invalid JSON syntax. Check commas and quotes.")
        raise
    except OSError as error:
        record.mark_failed(
            f"Could not read document ({type(error).__name__}). Check file access."
        )
        raise
    except (ValueError, csv.Error):
        record.mark_failed(
            "Invalid document data. Check the format and required transaction fields."
        )
        raise
    else:
        record.mark_completed()
        return transactions
