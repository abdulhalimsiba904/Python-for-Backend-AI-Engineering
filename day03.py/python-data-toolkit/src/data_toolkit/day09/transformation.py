"""Normalize only accepted batches and return fresh canonical dictionaries."""
from .validation import validate_transactions


def transform_transactions(records: list) -> list[dict]:
    """Trim IDs, collapse category whitespace/case, and convert amounts.

    No implicit numeric-string parsing; extra metadata is deliberately omitted.
    A bad direct call raises ValueError rather than silently dropping rows.
    """
    valid, invalid = validate_transactions(records)
    if invalid:
        raise ValueError(f"invalid transaction at row {invalid[0]['row']}")
    return [
        {"transaction_id": record["transaction_id"].strip(),
         "category": " ".join(record["category"].split()).casefold(),
         "amount": float(record["amount"])}
        for record in valid
    ]
