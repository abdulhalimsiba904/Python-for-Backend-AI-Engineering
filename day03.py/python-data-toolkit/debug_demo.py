def calculate_average(amounts):
    if not amounts:
        return None

    total = sum(amounts)
    average = total / len(amounts)
    return average


numbers = []

result = calculate_average(numbers)
print(f"Average: {result}")