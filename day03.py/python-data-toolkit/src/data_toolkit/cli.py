
import argparse
import json
import logging
from pathlib import Path
from uuid import uuid4

from data_toolkit.readers import read_csv, read_json
from data_toolkit.reports import calculate_average, count_categories
from data_toolkit.transformers import normalize_transactions
from data_toolkit.validators import find_duplicate_ids

logger = logging.getLogger(__name__)


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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read transaction data and generate a summary."
    )
    parser.add_argument(
        "file",
        nargs="?",
        default="samples/transactions.json",
        help="Path to a JSON or CSV transaction file.",
    )
    parser.add_argument("--verbose", action="store_true", help="Show safe progress logs.")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING,
                        format="%(message)s")
    run_id = uuid4().hex

    def log_event(level: int, event: str, **details) -> None:
        # Only pass allowlisted metadata: never records, IDs, values or paths.
        logger.log(level, json.dumps({"event": event, "run_id": run_id,
                                    "entry_point": "cli", **details}))

    log_event(logging.INFO, "load_started")
    try:
        transactions = load_transactions(args.file)
    except json.JSONDecodeError as error:
        log_event(logging.WARNING, "load_failed", error_type="JSONDecodeError")
        parser.error(f"Invalid JSON at line {error.lineno}, column {error.colno}. Check commas and quotes.")
    except (OSError, ValueError) as error:
        log_event(logging.WARNING, "load_failed", error_type=type(error).__name__)
        parser.error(str(error))
    else:
        log_event(logging.INFO, "load_succeeded", record_count=len(transactions))
    finally:
        log_event(logging.INFO, "load_attempt_finished")

    amounts = [transaction["amount"] for transaction in transactions]
    average = calculate_average(amounts)
    category_counts = count_categories(transactions)
    duplicate_ids = find_duplicate_ids(transactions)

    print("=== Python Data Toolkit ===")
    print(f"Input file: {args.file}")
    print(f"Transaction count: {len(transactions)}")
    print(f"Average amount: {average}")
    print(f"Category counts: {category_counts}")
    print(f"Duplicate IDs: {duplicate_ids}")


if __name__ == "__main__":
    main()

