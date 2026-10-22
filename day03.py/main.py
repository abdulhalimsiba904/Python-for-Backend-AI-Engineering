from calculations import calculate_total, calculate_average

amounts = [250.0, 400.0, 150.0]

total = calculate_total(amounts)
average = calculate_average(amounts)

print(f"Total: {total:.2f}")
print(f"Average: {average:.2f}")