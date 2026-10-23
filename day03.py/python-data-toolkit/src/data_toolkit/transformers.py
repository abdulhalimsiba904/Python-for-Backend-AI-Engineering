
def normalize_transactions(transactions: list[dict]) -> list[dict]:
    """Convert transaction amounts to floats and normalize their fields."""
    normalized = []

    for transaction in transactions:
        transaction_id = transaction.get("id")
        amount = transaction.get("amount")
        category = transaction.get("category")

        if not isinstance(transaction_id, str) or not transaction_id.strip():
            raise ValueError("Each transaction must have a non-empty ID.")

        if amount is None or isinstance(amount, bool):
            raise ValueError(
                f"Transaction {transaction_id} must have a valid amount."
            )

        try:
            numeric_amount = float(amount)
        except (TypeError, ValueError) as error:
            raise ValueError(
                f"Transaction {transaction_id} has an invalid amount: {amount!r}"
            ) from error

        if not isinstance(category, str) or not category.strip():
            raise ValueError(
                f"Transaction {transaction_id} must have a non-empty category."
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
