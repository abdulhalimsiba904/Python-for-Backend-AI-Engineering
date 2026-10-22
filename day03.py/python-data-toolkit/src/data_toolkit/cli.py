
from data_toolkit.reports import calculate_average, count_categories
from data_toolkit.validators import find_duplicate_ids


def main():
    transactions = [
        {"id": "TX1001", "amount": 100.0, "category": "food"},
        {"id": "TX1002", "amount": 50.0, "category": "transport"},
        {"id": "TX1003", "amount": 75.0, "category": "food"},
        {"id": "TX1001", "amount": 25.0, "category": "food"},
    ]

    amounts = [
        transaction["amount"]
        for transaction in transactions
    ]

    average = calculate_average(amounts)
    category_counts = count_categories(transactions)
    duplicate_ids = find_duplicate_ids(transactions)

    print("=== Python Data Toolkit ===")
    print(f"Transaction count: {len(transactions)}")
    print(f"Average amount: {average}")
    print(f"Category counts: {category_counts}")
    print(f"Duplicate IDs: {duplicate_ids}")


if __name__ == "__main__":
    main()
