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
is required.

## Problem 2: Safe JSON File Reader

`student_records.py` defines `load_student_records(file_path)`. It reads UTF-8
JSON using `json.load` and `with open`, which closes the file even if parsing
fails. A top-level list is returned unchanged, including an empty list.
Individual list items are not validated.

Missing files and malformed JSON raise meaningful `ValueError` messages that
include the file path. Specific `FileNotFoundError` and `json.JSONDecodeError`
handlers preserve the original exception with `raise ... from ...`.
Valid JSON with a non-list top-level value also raises `ValueError`.
Other file access errors, such as permission errors, propagate unchanged.

Example from this assessment directory:

```python
from student_records import load_student_records

records = load_student_records("students.json")
```

`students.json` contains Amina (UDS001, 85), Musa (UDS002, 72), and
Fatima (UDS003, 91), using `student_id`, `name`, and `score` keys.
`invalid_students.json` deliberately contains malformed JSON (a trailing
comma). `wrong_structure.json` deliberately contains a top-level object.

The test command above runs all three problems. For Problem 2 alone, run from
`day03.py/python-data-toolkit`:

```powershell
python -m unittest discover -s day07_assessment -p test_student_records.py -v
```

The eight new tests cover the sample records, an empty list, unchanged list
contents and Unicode, a missing file, malformed JSON, an empty file, a top-level
object, and other non-list values. They also check exception chaining.
Temporary files are cleaned up automatically. Only the standard library is
required.

## Problem 3: Mobile Money Transaction Analyzer

`transaction_analyzer.py` defines `count_transactions_by_category(transactions)`.
It accepts a list of transaction dictionaries and returns a dictionary mapping
normalized categories to transaction counts. An empty list returns `{}`.

Each string category is stripped of leading and trailing whitespace and
lowercased, so case variants count together. Missing categories, `None`,
non-string values, empty strings, and whitespace-only strings are skipped.
Internal spaces are preserved. The function does not change its input and
supports arbitrary category names without hardcoded results.

```python
from transaction_analyzer import count_transactions_by_category

transactions = [{"category": category} for category in
                ["Food", "Transport", "food", "Bills", " transport ", "FOOD"]]
count_transactions_by_category(transactions)
# {"food": 3, "transport": 2, "bills": 1}
```

Run Problem 3 alone from `day03.py/python-data-toolkit`:

```powershell
python -m unittest discover -s day07_assessment -p test_transaction_analyzer.py -v
```

The 11 tests cover the sample, empty input, a single category, missing keys,
empty and whitespace-only strings, `None` and other non-string values,
tabs and newlines, arbitrary categories and internal spaces, mixed valid and
invalid categories, preserving input, and independent calls. Only Python's
standard library is required. The loop takes O(n) time for n transactions
(plus string normalization) and O(k) extra space for k distinct categories.