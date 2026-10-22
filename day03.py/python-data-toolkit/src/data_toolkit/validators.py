def find_duplicate_ids(transactions: list[dict]) -> set[str]:
    """Return the transaction IDs that appear more than once."""
    seen_ids = set()
    duplicate_ids = set()

    for transaction in transactions:
        transaction_id = transaction.get("id")

        if not transaction_id:
            continue

        if transaction_id in seen_ids:
            duplicate_ids.add(transaction_id)
        else:
            seen_ids.add(transaction_id)

    return duplicate_ids