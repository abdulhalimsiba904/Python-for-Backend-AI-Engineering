
import argparse
from pathlib import Path

from data_toolkit.readers import read_csv, read_json
from data_toolkit.reports import calculate_average, count_categories
from data_toolkit.transformers import normalize_transactions
from data_toolkit.validators import find_duplicate_ids


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
    args = parser.parse_args()

    try:
        transactions = load_transactions(args.file)
    except (OSError, ValueError) as error:
        parser.error(str(error))

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

