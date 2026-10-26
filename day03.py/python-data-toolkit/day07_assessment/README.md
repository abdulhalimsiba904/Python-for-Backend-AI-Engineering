# Day 7 Assessment — Problem 1: Student Performance Statistics

`student_statistics.py` defines `calculate_statistics(scores)`. It accepts a
list of valid numeric scores and returns a dictionary without printing or
changing the input. Input validation is outside this problem's scope.

The function handles an empty list first, returning zero for total, count,
passed and failed, and `None` for average, highest and lowest. This avoids
division by zero and calling `min` or `max` on an empty list.

For a nonempty list, `sum` and `len` give the total and count. Their quotient
is the average, rounded with `round(..., 2)`. `max` and `min` give the extremes.
The loop counts each score of at least 50 as a pass; every remaining score
is a failure, so `failed = count - passed`. Each score belongs to exactly one
group. The work is O(n) with O(1) extra space.

For `[85, 72, 49, 90, 65, 38, 77]`, the result is:

```python
{
    "total": 476, "average": 68.0, "highest": 90, "lowest": 38,
    "count": 7, "passed": 5, "failed": 2,
}
```

Run from `day03.py/python-data-toolkit`:

```powershell
python -m unittest discover -s day07_assessment -v
```

The nine tests cover the example, empty input, one score at 50, all passing,
all failing (including zero), decimals around 50, average rounding, repeated
scores, and preserving input order and values. Only Python's standard library
is required. Problems 2 and 3 are not included.
