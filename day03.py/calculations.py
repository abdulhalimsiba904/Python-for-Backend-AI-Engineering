def calculate_total(amounts: list[float]) -> float:
    total = 0.0

    for amount in amounts:
        total += amount

    return total


def calculate_average(amounts: list[float]) -> float | None:
    if not amounts:
        return None

    total = calculate_total(amounts)
    return total / len(amounts)