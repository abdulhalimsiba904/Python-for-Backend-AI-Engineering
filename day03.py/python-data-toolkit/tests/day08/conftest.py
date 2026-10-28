"""Fresh input per test; no shared mutable transaction state."""
import pytest


@pytest.fixture
def transactions():
    return [
        {"id": " T1 ", "amount": "2", "category": " Food "},
        {"id": "T2", "amount": 4, "category": "FOOD"},
        {"id": "T2", "amount": 6, "category": "Transport"},
    ]
