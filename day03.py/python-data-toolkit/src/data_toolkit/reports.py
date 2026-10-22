#Calculate the average of a list of transaction amounts.
def calculate_average(amounts: list[float]) -> float | None:
    """Return the average of the amounts, or None if the list is empty."""
    if not amounts:
        return None

    total = sum(amounts)
    average = total / len(amounts)
    return round(average, 2)

#Counts how many transactions belong to each category
def count_categories(transactions: list[dict]) -> dict[str, int]:
    """Count the number of transactions in each category."""
    category_counts = {}

    for transaction in transactions:
        category = transaction["category"]

        if category not in category_counts:
            category_counts[category] = 0

        category_counts[category] += 1

    return category_counts