
from math import isfinite


def normalize_transactions(transactions: list[dict]) -> list[dict]:
    """Convert transaction amounts to floats and normalize their fields."""
    normalized = []

    for row_number, transaction in enumerate(transactions, start=1):
        transaction_id = transaction.get("id")
        amount = transaction.get("amount")
        category = transaction.get("category")

        if not isinstance(transaction_id, str) or not transaction_id.strip():
            raise ValueError(f"Transaction row {row_number} must have a non-empty ID.")

        if amount is None or isinstance(amount, bool):
            raise ValueError(
                f"Transaction row {row_number} must have a valid amount."
            )

        try:
            numeric_amount = float(amount)
        except (TypeError, ValueError, OverflowError):
            raise ValueError(
                f"Transaction row {row_number} has an invalid amount; use a number."
            ) from None

        if not isfinite(numeric_amount):
            raise ValueError(f"Transaction row {row_number} amount must be finite.")

        if not isinstance(category, str) or not category.strip():
            raise ValueError(
                f"Transaction row {row_number} must have a non-empty category."
            )

        normalized.append(
            {
                **transaction,
                "id": transaction_id.strip(),
                "amount": numeric_amount,
                "category": category.strip().lower(),
            }
        )

    return normalized
