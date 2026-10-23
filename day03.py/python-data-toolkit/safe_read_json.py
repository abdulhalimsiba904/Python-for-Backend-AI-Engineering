import json

file_path = "samples/transactions.json"

try:
    with open(file_path, "r", encoding="utf-8") as file:
        transactions = json.load(file)

except FileNotFoundError:
    print(f"Error: File not found: {file_path}")

except json.JSONDecodeError as error:
    print(f"Error: Invalid JSON: {error}")

else:
    print(f"Successfully loaded {len(transactions)} transactions.")