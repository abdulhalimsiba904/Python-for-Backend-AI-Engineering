import json

file_path = "samples/transactions.json"

with open(file_path, "r", encoding="utf-8") as file:
    transactions = json.load(file)

print(f"Number of transactions: {len(transactions)}")

for transaction in transactions:
    print(
        f"{transaction['id']}: "
        f"{transaction['amount']:.2f} "
        f"({transaction['category']})"
    )