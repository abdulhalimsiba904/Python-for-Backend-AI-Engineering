# Day 9 transaction contract and practical

Day 9 uses `data_toolkit.day09` and `transaction_id`. Earlier modules still use
`id`, accept numeric strings, and permit refunds and zero; their behavior is unchanged.

## Contract

- Input is a list of ordinary data dictionaries; other batch types raise TypeError.
- Required fields: transaction_id and category are nonblank strings; amount is an
  exact built-in int or float, positive, finite, and convertible to finite float.
- bool, numeric strings, None, zero, negative values, NaN, infinity and integer
  overflow during float conversion are rejected. Decimal and numeric subclasses
  are outside this teaching contract. Finite floats can lose decimal precision.
- IDs lose outer whitespace only; case and internal spaces remain meaningful.
- Categories collapse all whitespace runs to one space and use casefold().
- The first valid occurrence of a trimmed ID wins. An invalid first row does not
  reserve an ID. Later occurrences are rejected; IDs are case sensitive.
- All field problems in a row are collected. Errors contain a 1-based original
  row number and field messages, without raw values. Row numbers locate the source.
- Extra fields are optional, allowed and deep-copied during validation; they have
  no schema guarantees. Transformation deliberately emits only the three fields.
- Validation returns valid raw copies and invalid reports in input order.
  Transformation and statistics reject invalid direct calls with ValueError;
  they do not silently discard bad rows. Caller handles the invalid report.
- Transformation returns fresh dictionaries; it is idempotent. Functions never
  mutate input. Ordinary copyable data values are expected in extra metadata.
- Empty input is valid: count 0, total 0.0, mean/min/max None and no categories.
- Statistics use sorted math.fsum inputs, sorted category keys and unrounded
  floats. Same accepted records give the same summary regardless of their order.
  Reordering conflicting duplicates can change which row wins before aggregation.
  Aggregate overflow raises ValueError; this is an educational float pipeline,
  not financial accounting. Production money should use a specified Decimal or
  integer-minor-unit contract with currency and rounding rules.

## Run on Windows PowerShell

```powershell
Set-Location 'C:\Users\USER\python-foundations\day03.py\python-data-toolkit'
python --version
python day9_practicals.py
python -m pytest tests/day09 -v
python -m pytest -q
python run_day5_tests.py
```

Use a working Python 3.12 interpreter. If python is missing, use a verified
absolute path with `& $py`. Do not remove or replace the existing .venv.
pytest is already declared in requirements-dev.txt; no dependency changes.
For VS Code: open this toolkit folder, use Python: Select Interpreter, then
Python: Configure Tests > pytest > tests. The terminal full-suite command also
includes day07_assessment and test_toolkit.py via pytest.ini.

## Module walkthrough

1. `validation.py`: check shape, missing keys, text, amount, then duplicate IDs.
   A set makes duplicate lookup O(1) on average; scan is O(n) for fixed-size rows.
   Deep copying costs additional time and space proportional to metadata size.
2. `transformation.py`: revalidate to guard direct calls; map raw accepted rows
   to canonical dictionaries. No implicit repair of invalid values.
3. `statistics.py`: normalize, group by category, then count and sum. Sorting
   amounts guarantees a fixed addition order; overall O(n log n), O(n) space,
   plus validation/copy costs. A nested scan for duplicates would be O(n squared).
4. `day9_practicals.py`: show accepted records, rejects and summary separately.

## Expected demo

Two accepted transactions total 20.5; average 10.25; minimum 8.5; maximum 12.0.
Category food has count 2 and total 20.5. Rejected rows are 3 (duplicate ID),
4 (Boolean amount), and 5 (missing category and negative amount).

## Test coverage

`tests/day09/test_day09.py` tests valid data, full pipeline outputs, missing keys,
blank and wrong text types, non-dictionary rows, wrong batch types, Boolean and
numeric string amounts, nonpositive/nonfinite/oversized amounts, duplicate policy,
all-field reporting, empty input, deep-copy independence, transformation
idempotence, direct-call failures, sorted category keys, permutation-invariant
statistics and aggregate overflow. Use pytest.approx for decimal float results.

The old custom runner scans only tests/test_*.py. Day 9 pytest tests intentionally
live in a subdirectory like Day 8. Run pytest for the combined test suite.

## Independent practice

Before reading the implementation, write a contract, make one failing test,
implement one check and rerun it. Then add category cleaning, duplicate handling
and statistics. Explain why True passes isinstance(True, int), why bool amounts
must be rejected before arithmetic, and why an empty average is not zero.
