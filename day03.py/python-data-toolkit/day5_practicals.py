"""Run all Day 5 demonstrations without changing sample files."""
import json
from pathlib import Path

from data_toolkit.cli import load_transactions
from data_toolkit.reports import calculate_average
from data_toolkit.transformers import normalize_transactions

ROOT = Path(__file__).resolve().parent


def process_amount(text: str) -> float | None:
    """Show try, except, else and finally on both paths."""
    try:
        amount = float(text)
    except ValueError:
        print("Error: The amount must be a valid number.")
        return None
    else:
        print(f"Successfully processed amount: {amount}")
        return amount
    finally:
        print("Amount processing attempt finished.")


def validate_non_negative(amount: float) -> float:
    """An exercise rule; the toolkit still allows negative refunds."""
    if amount < 0:
        raise ValueError("Amount cannot be negative.")
    return amount


def broken_average(amounts: list[float]) -> float:
    """Deliberately broken for traceback investigation only."""
    return sum(amounts) / len(amounts)


def main() -> None:
    print("1. Exception flow: success and failure")
    assert process_amount("125.50") == 125.5
    assert process_amount("hello") is None
    print("2. Raising an exception")
    print(validate_non_negative(25.0))
    try:
        validate_non_negative(-1.0)
    except ValueError as error:
        print(f"Caught ValueError: {error}")

    print("3. Reproduce and fix an empty average")
    try:
        broken_average([])
    except ZeroDivisionError:
        print("Reproduced ZeroDivisionError: division by zero")
    print(f"Fixed empty average: {calculate_average([])}")
    assert calculate_average([10, 20, 30]) == 20.0

    print("4. Missing file and malformed JSON")
    for name in ["not_here.json", "malformed.json"]:
        try:
            load_transactions(ROOT / "samples" / name)
        except FileNotFoundError:
            print("FileNotFoundError: Check the file location and filename.")
        except json.JSONDecodeError as error:
            print(f"JSONDecodeError: Check line {error.lineno}, column {error.colno}.")

    print("5. Invalid number, missing field, Boolean and non-finite values")
    for record in [
        {"id": "T1", "amount": "hello", "category": "food"},
        {"id": "T1", "amount": 25},
        {"id": "T1", "amount": True, "category": "food"},
        {"id": "T1", "amount": "nan", "category": "food"},
    ]:
        try:
            normalize_transactions([record])
        except ValueError as error:
            print(f"ValueError: {error}")
    print("All Day 5 practicals finished.")


if __name__ == "__main__":
    main()
