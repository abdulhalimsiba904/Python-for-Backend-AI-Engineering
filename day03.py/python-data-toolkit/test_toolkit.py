from data_toolkit.reports import calculate_average, count_categories
from data_toolkit.validators import find_duplicate_ids




# Test 1: Calculate an average
amounts = [100.0, 200.0, 300.0]
result = calculate_average(amounts)
assert result == 200.0
print("Test 1 passed: calculate_average")

# Test 2: Handle an empty list
result = calculate_average([])
assert result is None
print("Test 2 passed: empty list")

# Test 3: Count categories
transactions = [
    {"category": "food", "amount": 100.0},
    {"category": "transport", "amount": 50.0},
    {"category": "food", "amount": 75.0},
]

result = count_categories(transactions)
assert result == {"food": 2, "transport": 1}
print("Test 3 passed: count_categories")

# Test 4: Find duplicate transaction IDs
transactions = [
    {"id": "TX1001", "amount": 100.0, "category": "food"},
    {"id": "TX1002", "amount": 200.0, "category": "transport"},
    {"id": "TX1001", "amount": 150.0, "category": "food"},
]

result = find_duplicate_ids(transactions)
assert result == {"TX1001"}
print("Test 4 passed: find_duplicate_ids")

# Test 5: Handle an empty transaction list
result = find_duplicate_ids([])
assert result == set()
print("Test 5 passed: empty transaction list")

print("\nAll tests passed!")