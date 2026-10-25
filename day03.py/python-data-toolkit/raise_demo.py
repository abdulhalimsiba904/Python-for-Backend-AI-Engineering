def validate_amount(amount: float) -> float:
    if amount < 0:
        raise ValueError("Amount cannot be negative.")

    return amount


print(validate_amount(25.0))