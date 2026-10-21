
# The data (TX1002 appears twice on purpose)
transactions = [
    {"id": "TX1001", "amount": 250.00, "category": "food"},
    {"id": "TX1002", "amount": 400.00, "category": "transport"},
    {"id": "TX1003", "amount": 150.00, "category": "food"},
    {"id": "TX1004", "amount": 300.00, "category": "utilities"},
    {"id": "TX1002", "amount": 200.00, "category": "food"},
]

# Step 1: Count the total number of records
total_records = len(transactions)

# Step 2: Total amount
total_amount = 0
for t in transactions:
    total_amount = total_amount + t["amount"]

# Step 3: Average amount
if total_records > 0:
    average_amount = total_amount / total_records
else:
    average_amount = 0


# Steps 4 and 5: Highest and lowest transaction
# Start by assuming the first one is both, then compare the rest.

highest = transactions[0]
lowest = transactions[0]

for t in transactions:
    if t["amount"] > highest["amount"]:
        highest = t
    if t["amount"] < lowest["amount"]:
        lowest = t


# Step 6: Count transactions in each category
category_counts = {}

for t in transactions:
    category = t["category"]
    if category in category_counts:
        category_counts[category] = category_counts[category] + 1
    else:
        category_counts[category] = 1


# Step 7: Detect duplicate IDs (and count unique IDs)
seen_ids = []        # IDs we have already looked at
duplicate_ids = []   # IDs that showed up more than once

for t in transactions:
    tx_id = t["id"]
    if tx_id in seen_ids:
        if tx_id not in duplicate_ids:
            duplicate_ids.append(tx_id)
    else:
        seen_ids.append(tx_id)

unique_id_count = len(seen_ids)


# Step 8: Filter - keep only transactions of $250 or more
minimum = 250
large_transactions = []

for t in transactions:
    if t["amount"] >= minimum:
        large_transactions.append(t)

# Step 9: Sort by amount, highest first
# (sorted() makes a new list; the original is unchanged)
sorted_transactions = sorted(transactions, key=lambda t: t["amount"], reverse=True)

# Step 10: Display the summary
print("=" * 40)
print("TRANSACTION SUMMARY")
print("=" * 40)

print()
print("Counts")
print("------")
print("Total records:", total_records)
print("Unique IDs:   ", unique_id_count)

print()
print("Amounts")
print("-------")
print(f"Total:   ${total_amount:.2f}")
print(f"Average: ${average_amount:.2f}")
print(f"Highest: {highest['id']} | ${highest['amount']:.2f} | {highest['category']}")
print(f"Lowest:  {lowest['id']} | ${lowest['amount']:.2f} | {lowest['category']}")
print()
print("Transactions per category")
print("-------------------------")
for category in category_counts:
    print(f"{category}: {category_counts[category]}")

print()
print("Duplicate IDs")
print("-------------")
if len(duplicate_ids) == 0:
    print("None found")
else:
    for tx_id in duplicate_ids:
        print(f"{tx_id} appears more than once")

print()
print(f"Transactions of ${minimum} or more")
print("-" * 30)
for t in large_transactions:
    print(f"{t['id']} | ${t['amount']:.2f} | {t['category']}")

print()
print("Sorted by amount (highest first)")
print("--------------------------------")
for t in sorted_transactions:
    print(f"{t['id']} | ${t['amount']:.2f} | {t['category']}")