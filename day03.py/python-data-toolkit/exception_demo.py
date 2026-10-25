try:
    amount = float("hello")
    print(f"Amount: {amount}")
except ValueError:
    print("Error: The amount must be a valid number.")

print("Program continues.")