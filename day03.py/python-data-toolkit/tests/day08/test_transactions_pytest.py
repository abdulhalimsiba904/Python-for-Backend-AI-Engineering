"""Strict toolkit validation differs from the forgiving Day 7 counter."""
from copy import deepcopy

import pytest

from data_toolkit.reports import count_categories
from data_toolkit.transformers import normalize_transactions
from data_toolkit.validators import find_duplicate_ids
from transaction_analyzer import count_transactions_by_category


def test_normalization_preserves_input_and_duplicate_records(transactions):
    original = deepcopy(transactions)
    normalized = normalize_transactions(transactions)
    assert normalized == [
        {"id": "T1", "amount": 2.0, "category": "food"},
        {"id": "T2", "amount": 4.0, "category": "food"},
        {"id": "T2", "amount": 6.0, "category": "transport"},
    ]
    assert transactions == original
    assert count_categories(normalized) == {"food": 2, "transport": 1}
    assert find_duplicate_ids(normalized) == {"T2"}
    normalized[0]["category"] = "changed"
    assert transactions == original


@pytest.mark.parametrize("field", ["id", "amount", "category"])
def test_missing_required_field_is_rejected(transactions, field):
    del transactions[0][field]
    with pytest.raises(ValueError, match=f"(?i){field}"):
        normalize_transactions(transactions)


@pytest.mark.parametrize("amount", [True, False, None, "bad", [], {},
                                         "nan", "inf", "-inf"])
def test_regression_invalid_amounts_are_rejected(transactions, amount):
    # Python treats bool as numeric; the input boundary must reject it.
    transactions[0]["amount"] = amount
    with pytest.raises(ValueError, match="amount"):
        normalize_transactions(transactions)


def test_regression_errors_do_not_disclose_private_input(transactions):
    transactions[0]["amount"] = "PRIVATE-TOKEN"
    with pytest.raises(ValueError) as caught:
        normalize_transactions(transactions)
    assert "PRIVATE-TOKEN" not in str(caught.value)
    assert "row 1" in str(caught.value)


def test_calls_do_not_share_category_counts():
    assert count_categories([{"category": "food"}]) == {"food": 1}
    assert count_categories([{"category": "bills"}]) == {"bills": 1}


@pytest.mark.parametrize("category", [None, "", " ", 5, True])
def test_day7_counter_skips_invalid_categories(category):
    rows = [{}, {"category": category}, {"category": " Food "}]
    original = deepcopy(rows)
    assert count_transactions_by_category(rows) == {"food": 1}
    assert rows == original


def test_toolkit_counter_requires_category_field():
    with pytest.raises(KeyError, match="category"):
        count_categories([{}])
