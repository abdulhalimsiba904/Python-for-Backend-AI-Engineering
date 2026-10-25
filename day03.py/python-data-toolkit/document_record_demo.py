"""Demonstrate Day 6 objects and composition without changing sample files."""
from pathlib import Path
import sys
from uuid import uuid4

ROOT = Path(__file__).resolve().parent
# Like the test runner, find src without requiring terminal configuration.
sys.path.insert(0, str(ROOT / "src"))

from data_toolkit.models import DocumentRecord
from data_toolkit.processing import process_document
from data_toolkit.reports import calculate_average, count_categories


def demonstrate_objects() -> None:
    """Show independent attributes, instance methods, and state changes."""
    print("1. Classes, objects, attributes, and methods")
    # DocumentRecord is the class. Calling it creates an object (an instance).
    # Its constructor (__init__) initializes attributes on that instance.
    first = DocumentRecord("DEMO-001", "first.json", "json")
    second = DocumentRecord("DEMO-002", "second.csv", "csv")
    print(f"Filename attribute: {first.filename}")
    print(f"Initial state: {first.get_summary()}")
    # In each method, self refers to the instance on the left of the dot.
    first.mark_processing()
    print(f"Status after mark_processing(): {first.processing_status}")
    first.mark_completed()
    print(f"After mark_completed(): {first.get_summary()}")

    second.add_validation_error("Example: required amount is missing.")
    print(f"Independent second object: {second.get_summary()}")
    print(f"First object's errors: {first.validation_errors}")
    print(f"Second object's errors: {second.validation_errors}")
    print(f"Second object is valid: {second.is_valid()}")
    try:
        second.mark_completed()
    except ValueError as error:
        print(f"Invalid completion prevented: {error}")


def demonstrate_composition() -> None:
    """Combine record objects with existing readers and report functions."""
    print("\n2. Composition with the existing JSON and CSV toolkit")
    for suffix in ("json", "csv"):
        path = ROOT / "samples" / f"transactions.{suffix}"
        # Generate unique labels for actual processing attempts.
        record = DocumentRecord(uuid4().hex, path.name, suffix)
        print(f"Before processing: {record.get_summary()}")
        transactions = process_document(record, path)
        print(f"After processing: {record.get_summary()}")
        amounts = [transaction["amount"] for transaction in transactions]
        print(f"Average amount: {calculate_average(amounts)}")
        print(f"Category counts: {count_categories(transactions)}")

    print("\n3. Failed processing with a safe stored error")
    path = ROOT / "samples" / "malformed.json"
    record = DocumentRecord(uuid4().hex, path.name, "json")
    try:
        process_document(record, path)
    except ValueError:
        # Show the curated message, not raw document content or exception data.
        print(record.get_summary())
        print(f"Validation errors: {record.validation_errors}")


def main() -> None:
    """Run the self-contained Day 6 demonstrations."""
    demonstrate_objects()
    demonstrate_composition()


if __name__ == "__main__":
    main()
