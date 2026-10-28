"""Numeric helpers accept numeric lists; validation belongs at input boundaries."""
import pytest

from data_toolkit.reports import calculate_average
from student_statistics import calculate_statistics


def test_average_of_numbers():
    assert calculate_average([2, 4, 6]) == 4


@pytest.mark.parametrize("amounts, expected", [
    ([], None), ([0], 0), ([2, 2, 8], 4),
    ([-5, 0, 5], 0), ([1, 2, 2], 1.67),
], ids=["empty", "zero", "duplicates-count", "refunds", "rounding"])
def test_average_contract(amounts, expected):
    assert calculate_average(amounts) == expected


@pytest.mark.parametrize("amounts", [["2", "4"], [2, None]])
def test_average_does_not_convert_wrong_element_types(amounts):
    with pytest.raises(TypeError):
        calculate_average(amounts)


@pytest.mark.parametrize("scores, expected", [
    ([], {"total": 0, "average": None, "highest": None, "lowest": None,
          "count": 0, "passed": 0, "failed": 0}),
    ([49, 50, 50], {"total": 149, "average": 49.67, "highest": 50,
                    "lowest": 49, "count": 3, "passed": 2, "failed": 1}),
])
def test_statistics_contract(scores, expected):
    original = scores.copy()
    assert calculate_statistics(scores) == expected
    assert scores == original


def test_statistics_wrong_element_type():
    with pytest.raises(TypeError):
        calculate_statistics([50, "60"])
