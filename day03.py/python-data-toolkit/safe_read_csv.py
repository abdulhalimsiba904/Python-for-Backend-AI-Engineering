import csv

file_path = "samples/transactions.csv"

try:
    with open(file_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        transactions = list(reader)

except FileNotFoundError:
    print(f"Error: File not found: {file_path}")

else:
    print(f"Successfully loaded {len(transactions)} transactions.")