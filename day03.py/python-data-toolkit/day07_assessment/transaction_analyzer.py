"""Count mobile money transactions by their normalized categories."""


def count_transactions_by_category(transactions):
    """Count nonempty string categories, ignoring case and outer whitespace.

    Each transaction must be a dictionary. Missing or non-string categories
    are skipped, and the input is left unchanged.
    """
    counts = {}
    for transaction in transactions:
        category = transaction.get("category")
        if not isinstance(category, str):
            continue
        category = category.strip().lower()
        if category:
            counts[category] = counts.get(category, 0) + 1
    return counts
