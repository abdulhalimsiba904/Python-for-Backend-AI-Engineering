import csv

file_path = "samples/transactions.csv"

with open(file_path, "r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)

    transactions = list(reader)

print(f"Number of transactions: {len(transactions)}")

for transaction in transactions:
    print(
        f"{transaction['id']}: "
        f"{transaction['amount']} "
        f"({transaction['category']})"
    )