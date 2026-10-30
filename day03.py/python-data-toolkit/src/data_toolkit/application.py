"""Day 10 adapters: file I/O around reusable Day 9 business functions."""
import json
import os
from pathlib import Path
import tempfile

from data_toolkit.readers import read_csv, read_json
from data_toolkit.reports import calculate_average, count_categories
from data_toolkit.day09.validation import validate_transactions
from data_toolkit.day09.transformation import transform_transactions
from data_toolkit.day09.statistics import summarize_transactions


class InvalidTransactions(ValueError):
    """A rejected batch, containing safe row/field diagnostics only."""


def load_records(path: Path) -> list[dict]:
    """Adapt CSV strings and historical IDs; JSON keeps strict numeric types."""
    suffix = path.suffix.lower()
    if suffix not in {".csv", ".json"}:
        raise ValueError("Use a .csv or .json input file.")
    rows = read_csv(path) if suffix == ".csv" else read_json(path)
    adapted = []
    for number, original in enumerate(rows, 1):
        row = dict(original)
        if None in row:
            raise InvalidTransactions(f"Row {number}: too many CSV fields.")
        if "id" in row and "transaction_id" in row:
            if row["id"] != row["transaction_id"]:
                raise InvalidTransactions(f"Row {number}: conflicting ID fields.")
        if "transaction_id" not in row and "id" in row:
            row["transaction_id"] = row["id"]
        if suffix == ".csv" and isinstance(row.get("amount"), str):
            try:
                row["amount"] = float(row["amount"])
            except (ValueError, OverflowError):
                # Leave invalid text for Day 9's safe field diagnostics.
                pass
        adapted.append(row)
    return adapted


def accepted_records(path: Path) -> list[dict]:
    """Reject the whole batch if any row fails; never silently lose records."""
    valid, invalid = validate_transactions(load_records(path))
    if invalid:
        details = [f"Row {item['row']}: " + "; ".join(
            f"{field}: {message}" for field, message in item["errors"].items()
        ) for item in invalid]
        raise InvalidTransactions("\n".join(details))
    return transform_transactions(valid)


def render_report(records: list[dict]) -> str:
    """Pure text formatting using both Day 9 and earlier report functions."""
    records = transform_transactions(records)
    summary = summarize_transactions(records)
    counts = count_categories(records)
    average = calculate_average([row["amount"] for row in records])
    lines = ["Python Data Toolkit Report", f"Count: {summary['count']}",
             f"Total: {summary['total']:.2f}",
             f"Average (2 decimals): {average if average is not None else 'N/A'}",
             f"Minimum: {summary['minimum']}", f"Maximum: {summary['maximum']}",
             "Categories:"]
    for category, values in summary["by_category"].items():
        lines.append(f"  {category}: count={counts[category]}, total={values['total']:.2f}")
    return "\n".join(lines) + "\n"


def write_output(destination: Path, text: str, source: Path, force: bool = False) -> None:
    """Publish a complete UTF-8 file; no overwrite unless explicitly requested.

    A same-directory temporary file avoids partial destination contents.
    Hard-link publication refuses concurrent existing destinations. --force
    uses replace. Requires normal local filesystem link/rename support.
    """
    if destination.resolve() == source.resolve():
        raise ValueError("Output must differ from input.")
    if destination.is_symlink():
        raise ValueError("Output must not be a symbolic link.")
    if source.exists() and destination.exists() and os.path.samefile(source, destination):
        raise ValueError("Output must differ from input.")
    if destination.exists() and not force:
        raise FileExistsError("Output exists; use --force to replace it.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=destination.parent,
            prefix=".data-toolkit-", suffix=".tmp", delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        if force:
            os.replace(temporary, destination)
        else:
            os.link(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def json_text(value: object) -> str:
    """Strict JSON with a final newline for tools and version control."""
    return json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False) + "\n"
