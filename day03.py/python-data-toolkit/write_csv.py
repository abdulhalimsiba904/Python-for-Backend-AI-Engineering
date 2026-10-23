import csv

transactions = [
    {"id": "TX1001", "amount": 100.0, "category": "food"},
    {"id": "TX1002", "amount": 50.0, "category": "transport"},
    {"id": "TX1003", "amount": 75.0, "category": "food"},
]

file_path = "output/transactions_export.csv"

fieldnames = ["id", "amount", "category"]

with open(file_path, "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(transactions)

print(f"CSV file saved to {file_path}")