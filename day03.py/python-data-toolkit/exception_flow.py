try:
    amount = float("125.50")

except ValueError:
    print("Error: Invalid amount.")

else:
    print(f"Successfully processed amount: {amount}")

finally:
    print("Amount processing attempt finished.")