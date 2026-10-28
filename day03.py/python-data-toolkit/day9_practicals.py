"""Run Day 9 from the toolkit root without configuring PYTHONPATH."""
from pathlib import Path
from pprint import pprint
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from data_toolkit.day09.validation import validate_transactions
from data_toolkit.day09.transformation import transform_transactions
from data_toolkit.day09.statistics import summarize_transactions


def main():
    records = [
        {"transaction_id": " T1 ", "category": " Food ", "amount": 12},
        {"transaction_id": "T2", "category": "FOOD", "amount": 8.5},
        {"transaction_id": "T1", "category": "food", "amount": 20},
        {"transaction_id": "T3", "category": "travel", "amount": True},
        {"transaction_id": "T4", "amount": -2},
    ]
    valid, invalid = validate_transactions(records)
    print("Accepted normalized transactions")
    clean = transform_transactions(valid)
    pprint(clean, sort_dicts=False)
    print("Invalid records with original row numbers")
    pprint(invalid, sort_dicts=False)
    print("Statistics for accepted records only")
    pprint(summarize_transactions(clean), sort_dicts=False)


if __name__ == "__main__":
    main()
