
from data_toolkit.transformers import normalize_transactions


def test_normalize_transactions():
    transactions = [
        {
            "id": " TX1001 ",
            "amount": "100.0",
            "category": " Food ",
        },
        {
            "id": "TX1002",
            "amount": 50,
            "category": "TRANSPORT",
        },
    ]

    result = normalize_transactions(transactions)

    assert result[0]["id"] == "TX1001"
    assert result[0]["amount"] == 100.0
    assert result[0]["category"] == "food"

    assert result[1]["amount"] == 50.0
    assert result[1]["category"] == "transport"

    # The original data should remain unchanged.
    assert transactions[0]["id"] == " TX1001 "
    assert transactions[0]["amount"] == "100.0"


def test_normalize_transactions_rejects_invalid_amount():
    transactions = [
        {
            "id": "TX1003",
            "amount": "not-a-number",
            "category": "food",
        }
    ]

    try:
        normalize_transactions(transactions)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for an invalid amount.")


def test_normalize_transactions_rejects_missing_id():
    transactions = [
        {
            "amount": 25.0,
            "category": "food",
        }
    ]

    try:
        normalize_transactions(transactions)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for a missing ID.")


if __name__ == "__main__":
    test_normalize_transactions()
    test_normalize_transactions_rejects_invalid_amount()
    test_normalize_transactions_rejects_missing_id()

    print("All transformer tests passed.")
