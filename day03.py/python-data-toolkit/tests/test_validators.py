
from data_toolkit.validators import find_duplicate_ids


def test_no_duplicate_ids():
    transactions = [
        {"id": "TX1001"},
        {"id": "TX1002"},
        {"id": "TX1003"},
    ]

    assert find_duplicate_ids(transactions) == set()


def test_one_duplicate_id():
    transactions = [
        {"id": "TX1001"},
        {"id": "TX1002"},
        {"id": "TX1001"},
    ]

    assert find_duplicate_ids(transactions) == {"TX1001"}


def test_multiple_duplicate_ids():
    transactions = [
        {"id": "TX1001"},
        {"id": "TX1002"},
        {"id": "TX1001"},
        {"id": "TX1002"},
        {"id": "TX1003"},
    ]

    assert find_duplicate_ids(transactions) == {"TX1001", "TX1002"}


def test_empty_transaction_list():
    assert find_duplicate_ids([]) == set()


def test_missing_and_empty_ids_are_ignored():
    transactions = [
        {"id": "TX1001"},
        {"id": ""},
        {},
        {"id": "TX1001"},
    ]

    assert find_duplicate_ids(transactions) == {"TX1001"}


if __name__ == "__main__":
    test_no_duplicate_ids()
    test_one_duplicate_id()
    test_multiple_duplicate_ids()
    test_empty_transaction_list()
    test_missing_and_empty_ids_are_ignored()

    print("All duplicate-ID tests passed!")
