
from data_toolkit.reports import calculate_average, count_categories


# Tests for calculate_average()

def test_average_of_multiple_amounts():
    assert calculate_average([100.0, 200.0, 300.0]) == 200.0


def test_average_of_one_amount():
    assert calculate_average([75.0]) == 75.0


def test_average_of_empty_list():
    assert calculate_average([]) is None


def test_average_rounds_to_two_decimal_places():
    assert calculate_average([10.0, 10.01]) == 10.0


# Tests for count_categories()

def test_counts_categories():
    transactions = [
        {"category": "food"},
        {"category": "transport"},
        {"category": "food"},
        {"category": "utilities"},
        {"category": "food"},
    ]

    expected = {
        "food": 3,
        "transport": 1,
        "utilities": 1,
    }

    assert count_categories(transactions) == expected


def test_empty_transaction_list():
    assert count_categories([]) == {}


if __name__ == "__main__":
    test_average_of_multiple_amounts()
    test_average_of_one_amount()
    test_average_of_empty_list()
    test_average_rounds_to_two_decimal_places()
    test_counts_categories()
    test_empty_transaction_list()

    print("All report tests passed!")
