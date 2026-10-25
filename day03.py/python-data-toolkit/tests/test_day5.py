"""Day 5 regression checks: plain functions and assertions, no unittest."""
from data_toolkit.transformers import normalize_transactions


def test_rejects_non_finite_amounts() -> None:
    for amount in ["nan", "inf", "-inf", 1e400]:
        try:
            normalize_transactions([{"id": "T1", "amount": amount, "category": "food"}])
        except ValueError as error:
            assert "finite" in str(error)
        else:
            raise AssertionError(f"Accepted non-finite amount: {amount}")


def test_errors_do_not_echo_private_values() -> None:
    try:
        normalize_transactions([{"id": "PRIVATE-ID", "amount": "PRIVATE-TOKEN", "category": "food"}])
    except ValueError as error:
        assert "PRIVATE" not in str(error)
        assert "row 1" in str(error)
    else:
        raise AssertionError("Expected an invalid amount error")


def test_missing_fields_and_boolean() -> None:
    valid = {"id": "T1", "amount": "25", "category": "food"}
    for field in valid:
        record = valid.copy()
        del record[field]
        try:
            normalize_transactions([record])
        except ValueError as error:
            assert field.lower() in str(error).lower()
        else:
            raise AssertionError(f"Accepted missing {field}")
    try:
        normalize_transactions([{**valid, "amount": True}])
    except ValueError:
        pass
    else:
        raise AssertionError("Accepted a Boolean as an amount")


def test_zero_refunds_and_extra_fields_still_work() -> None:
    records = [{"id": " T1 ", "amount": 0, "category": " Food ", "note": "kept"},
               {"id": "T2", "amount": "-5", "category": "food"}]
    result = normalize_transactions(records)
    assert result[0] == {"id": "T1", "amount": 0.0, "category": "food", "note": "kept"}
    assert result[1]["amount"] == -5.0
    assert records[0]["id"] == " T1 "


if __name__ == "__main__":
    test_rejects_non_finite_amounts()
    test_errors_do_not_echo_private_values()
    test_missing_fields_and_boolean()
    test_zero_refunds_and_extra_fields_still_work()
    print("All Day 5 validation tests passed.")
