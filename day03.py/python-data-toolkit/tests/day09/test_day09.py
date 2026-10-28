"""Day 9 contract tests; run from the toolkit root with pytest."""
from copy import deepcopy
from itertools import permutations

import pytest

from data_toolkit.day09.validation import validate_transactions
from data_toolkit.day09.transformation import transform_transactions
from data_toolkit.day09.statistics import summarize_transactions


def row(**changes):
    return {"transaction_id": " T1 ", "category": " Food  SHOP ",
            "amount": 12, **changes}


def test_pipeline_and_input_independence():
    raw = [row(extra={"tags": ["private"]}), row(transaction_id="T2", amount=8)]
    before = deepcopy(raw)
    valid, invalid = validate_transactions(raw)
    clean = transform_transactions(valid)
    assert invalid == []
    assert clean == [
        {"transaction_id": "T1", "category": "food shop", "amount": 12.0},
        {"transaction_id": "T2", "category": "food shop", "amount": 8.0}]
    assert summarize_transactions(clean) == {
        "count": 2, "total": 20.0, "average": 10.0,
        "minimum": 8.0, "maximum": 12.0,
        "by_category": {"food shop": {"count": 2, "total": 20.0}}}
    valid[0]["extra"]["tags"].append("changed")
    clean[0]["category"] = "changed"
    assert raw == before


@pytest.mark.parametrize("amount", [True, False, "12", "", None, [], {},
                                     0, -1, -0.0, float("nan"),
                                     float("inf"), -float("inf"), 10**400])
def test_bad_amounts(amount):
    valid, invalid = validate_transactions([row(amount=amount)])
    assert valid == []
    assert invalid[0]["row"] == 1
    assert "amount" in invalid[0]["errors"]


@pytest.mark.parametrize("field", ["transaction_id", "category", "amount"])
def test_missing_required_fields(field):
    record = row()
    del record[field]
    valid, invalid = validate_transactions([record])
    assert not valid
    assert invalid[0]["errors"][field] == "required field is missing"


@pytest.mark.parametrize("field", ["transaction_id", "category"])
@pytest.mark.parametrize("value", [None, "", " \t\n ", 12, True, [], {}])
def test_bad_text(field, value):
    valid, invalid = validate_transactions([row(**{field: value})])
    assert valid == []
    assert field in invalid[0]["errors"]


@pytest.mark.parametrize("value", [None, [], "wrong", 7, True])
def test_non_dictionary_rows(value):
    valid, invalid = validate_transactions([value])
    assert valid == []
    assert invalid == [{"row": 1, "errors": {"record": "must be a dictionary"}}]


@pytest.mark.parametrize("value", [None, {}, "wrong", (row(),)])
def test_batch_must_be_list(value):
    with pytest.raises(TypeError, match="list"):
        validate_transactions(value)


def test_duplicates_use_first_valid_trimmed_case_sensitive_id():
    raw = [row(amount=-1), row(), row(transaction_id="T1"),
           row(transaction_id="t1"), row(transaction_id="T1", amount=None)]
    valid, invalid = validate_transactions(raw)
    assert [r["transaction_id"] for r in valid] == [" T1 ", "t1"]
    assert [r["row"] for r in invalid] == [1, 3, 5]
    assert invalid[1]["errors"] == {"transaction_id": "duplicate ID"}
    assert set(invalid[2]["errors"]) == {"amount", "transaction_id"}


def test_reports_all_field_errors_without_echoing_values():
    _, invalid = validate_transactions([row(transaction_id=None, category=[], amount="SECRET")])
    assert set(invalid[0]["errors"]) == {"transaction_id", "category", "amount"}
    assert "SECRET" not in str(invalid)


def test_empty_dataset():
    assert validate_transactions([]) == ([], [])
    assert transform_transactions([]) == []
    assert summarize_transactions([]) == {
        "count": 0, "total": 0.0, "average": None,
        "minimum": None, "maximum": None, "by_category": {}}


def test_transform_is_idempotent_and_does_not_mutate():
    raw = [row()]
    before = deepcopy(raw)
    clean = transform_transactions(raw)
    assert transform_transactions(clean) == clean
    assert raw == before


@pytest.mark.parametrize("function", [transform_transactions, summarize_transactions])
def test_direct_consumers_reject_invalid_batches(function):
    with pytest.raises(ValueError, match="row 1"):
        function([row(amount=False)])
    with pytest.raises(ValueError, match="row 2"):
        function([row(), row()])


def test_statistics_normalizes_groups_and_is_order_independent():
    records = [row(transaction_id="A", amount=0.1, category=" Z "),
               row(transaction_id="B", amount=0.2, category="z"),
               row(transaction_id="C", amount=2, category=" A ")]
    before = deepcopy(records)
    expected = summarize_transactions(records)
    assert list(expected["by_category"]) == ["a", "z"]
    assert expected["by_category"]["z"]["total"] == pytest.approx(0.3)
    for order in permutations(records):
        assert summarize_transactions(list(order)) == expected
    assert records == before


def test_aggregate_overflow_is_explicit():
    records = [row(transaction_id="A", amount=1e308),
               row(transaction_id="B", amount=1e308)]
    with pytest.raises(ValueError, match="total"):
        summarize_transactions(records)
