import json

transactions = [
    {"id": "TX1001", "amount": 100.0, "category": "food"},
    {"id": "TX1002", "amount": 50.0, "category": "transport"},
    {"id": "TX1003", "amount": 75.0, "category": "food"},
]

file_path = "output/transactions_export.json"

with open(file_path, "w", encoding="utf-8") as file:
    json.dump(transactions, file, indent=4)

print(f"JSON file saved to {file_path}")