# Python Foundations — Day 5

## Test-runner follow-up

In a fresh PowerShell session, `python run_day5_tests.py` previously raised
`ModuleNotFoundError: No module named 'data_toolkit'`: the runner depended on
a manually configured `PYTHONPATH`. It now adds its own `src` folder to
Python's module search path before loading tests. A regression test launches
the targeted runner in a subprocess with `PYTHONPATH` removed. The updated
full suite contains 25 test functions plus the original five smoke assertions.
The earlier 24-function results below describe the initial Day 5 verification.
Application and individual test-script commands still need the documented
`PYTHONPATH` setup.

## Goal and three-hour schedule

Today you learn to make failures understandable, investigate them, and prove your fixes work. We use functions, dictionaries, lists, modules and plain `assert` tests. No custom classes or `unittest` are needed.

| Time | Topic | Practical outcome |
|---|---|---|
| 0:00–0:40 | Exceptions and validation | Handle invalid input; use `else`, `finally` and `raise` |
| 0:40–1:15 | Tracebacks and debugging | Investigate empty averages and missing files |
| 1:15–1:45 | Real data errors | Diagnose malformed JSON, invalid amounts and missing fields |
| 1:45–2:10 | Logging | Follow successful and failed loads without exposing secrets |
| 2:10–2:30 | Type hints | Explain function inputs, results and `None` |
| 2:30–2:55 | Debugger and targeted tests | Inspect variables and protect fixes with assertions |
| 2:55–3:00 | Recap | Explain the debugging process in your own words |

## Setup

Open PowerShell in your existing project:

```powershell
Set-Location 'C:\Users\USER\python-foundations\day03.py\python-data-toolkit'
$env:PYTHONPATH = 'src'
python --version
```

The verification session could not resolve `python`, and the existing `.venv` referred to an unavailable Windows Store Python installation. Verification therefore used the app's bundled Python 3.12.14. Your environment was not deleted or rebuilt. If `python` is unavailable in your terminal, use the verified interpreter for this session:

```powershell
$py = 'C:\Users\USER\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $py --version
& $py day5_practicals.py
```

In the remaining commands, replace `python` with `& $py` if necessary. These commands assume the project folder is your current folder. `PYTHONPATH` tells Python where the `data_toolkit` package lives; it does not install a package.

## 1. What an exception means

An exception is Python's way of reporting that an operation could not finish normally. Without a matching handler, execution stops and Python prints a traceback.

| Exception | Typical cause |
|---|---|
| `ValueError` | A value has the right general kind but cannot be used, such as `float('hello')` |
| `TypeError` | An operation receives an unsuitable type, such as `float(None)` |
| `ZeroDivisionError` | Division by zero |
| `FileNotFoundError` | A requested file is absent |
| `PermissionError` | Access to a file is denied |
| `json.JSONDecodeError` | Text is not valid JSON; this is also a `ValueError` |
| `KeyError` | A dictionary key accessed with square brackets is absent |

A syntax error prevents Python from understanding the program. A logic error can produce the wrong answer without raising anything. Tests are useful for all three situations, but exception handling does not automatically fix logic mistakes.

## 2. `try` and `except`: handle an expected failure

Your `exception_demo.py` demonstrates:

```python
try:
    amount = float('hello')
    print(f'Amount: {amount}')
except ValueError:
    print('Error: The amount must be a valid number.')

print('Program continues.')
```

Verified output:

```text
Error: The amount must be a valid number.
Program continues.
```

Python tries the conversion. It fails, skips the remaining statements in `try`, runs the matching `except`, then continues after the handler. Catch specific exceptions. A bare `except:` can hide programming bugs and catch interruptions you did not intend to handle.

Keep `try` small so it is clear which operation might fail. Handling an error means choosing a sensible response; it does not mean silently ignoring the problem.

## 3. `else` and `finally`: success and cleanup

Your `exception_flow.py` uses this structure:

```python
try:
    amount = float('125.50')
except ValueError:
    print('Error: Invalid amount.')
else:
    print(f'Successfully processed amount: {amount}')
finally:
    print('Amount processing attempt finished.')
```

Verified output:

```text
Successfully processed amount: 125.5
Amount processing attempt finished.
```

`else` runs only when the `try` block finishes without an exception. Exceptions inside `else` are not handled by that preceding `except`. `finally` runs as control leaves the statement, including during a return or an exception. It is useful for cleanup or reporting that an attempt finished. It does not mean the operation succeeded. Abrupt process termination can prevent cleanup.

The new `process_amount()` exercise in `day5_practicals.py` runs both paths. With `'hello'`, its output is:

```text
Error: The amount must be a valid number.
Amount processing attempt finished.
```

It returns `None` on that failure. A file opened with `with` is automatically closed when its block ends, even when an exception occurs. Prefer `with` over manually closing ordinary files in `finally`.

## 4. `raise`: enforce a rule deliberately

```python
def validate_non_negative(amount: float) -> float:
    if amount < 0:
        raise ValueError('Amount cannot be negative.')
    return amount
```

The practical calls this with `25.0` and `-1.0`:

```text
25.0
Caught ValueError: Amount cannot be negative.
```

`raise` stops the current normal path and sends an exception to the caller. The caller decides how to report or handle it. The original `raise_demo.py` still prints `25.0`.

This non-negative rule belongs to the exercise. The toolkit continues to accept finite negative amounts because they can represent refunds. Validation rules must match the application's needs.

`raise ValueError('clear explanation') from original_error` preserves the causal chain. When the original conversion error contains private input, displaying that chain can expose it. The toolkit's invalid-number handler uses `from None` to suppress that automatic display and reports a row number instead. This is not a general-purpose secret scrubber; do not print exception internals or local variables containing real secrets.

## 5. Read a traceback from the bottom up

The deliberately broken exercise is:

```python
def broken_average(amounts: list[float]) -> float:
    return sum(amounts) / len(amounts)

broken_average([])
```

To reproduce its uncaught failure without breaking the working toolkit:

```powershell
python -c "from day5_practicals import broken_average; broken_average([])"
```

The traceback ends with:

```text
    return sum(amounts) / len(amounts)
ZeroDivisionError: division by zero
```

Read the exception type and message first. Then find the closest project filename and line. Trace earlier frames to see which call supplied the bad input. Line numbers depend on the file version.

For an empty list, `sum([])` is `0` and `len([])` is `0`, so the expression attempts `0 / 0`.

Your working toolkit already contains the correct empty-list guard:

```python
def calculate_average(amounts: list[float]) -> float | None:
    if not amounts:
        return None
    total = sum(amounts)
    average = total / len(amounts)
    return round(average, 2)
```

Verified examples: `[10, 20, 30]` gives `20.0`; `[]` gives `None`. `None` means no average is available. Returning `0` would incorrectly suggest the average was measured as zero. The existing `debug_demo.py` still prints `Average: None`.

## 6. Missing-file investigation

```python
from pathlib import Path

file_path = Path('samples/not_here.json')
try:
    with file_path.open('r', encoding='utf-8') as file:
        contents = file.read()
except FileNotFoundError:
    print(f'Error: The file was not found: {file_path}')
else:
    print(contents)
print('Program continues.')
```

This is your existing `missing_file_demo.py`. It now remains a working example of recovery. The handler does not create or overwrite the missing file.

A relative path is resolved from the terminal's current folder, not automatically from the script's folder. Check `Path.cwd()`, the spelling, extension and directory before changing code. The new combined practical uses `Path(__file__).resolve().parent` to locate its sample folder reliably.

The CLI exits with status `2` for an expected input error. A successful CLI run exits with `0`. Other programs and scripts can use these statuses to detect failure.

## 7. Malformed JSON investigation

```python
import json
from pathlib import Path

try:
    with Path('samples/malformed.json').open(encoding='utf-8') as file:
        data = json.load(file)
except json.JSONDecodeError as error:
    print(f'Invalid JSON at line {error.lineno}, column {error.colno}.')
```

The existing malformed sample has a trailing comma after its last property. It is intentionally retained as an exercise fixture. JSON requires double quotes around property names and text values, and does not allow trailing commas. JSON uses `true`, `false` and `null`; Python uses `True`, `False` and `None`.

Verified toolkit command:

```powershell
python -m data_toolkit.cli samples/malformed.json
```

The error includes:

```text
Invalid JSON at line 6, column 5. Check commas and quotes.
```

The reader still raises the original `JSONDecodeError` for a caller that wants its location. The CLI catches it before `ValueError`, because the more general handler would also match it. Valid JSON can still have the wrong structure: `{}` is valid JSON but the toolkit requires a list of dictionaries. Syntax checking and data validation are separate steps.

## 8. Invalid amounts and missing fields

`normalize_transactions()` checks each record before reporting uses it. An ID and category must be non-empty strings. An amount must be convertible to a finite floating-point number and must not be a Boolean.

```python
amount = transaction.get('amount')
if amount is None or isinstance(amount, bool):
    raise ValueError('A valid amount is required.')
```

`transaction['amount']` raises `KeyError` when absent. `.get('amount')` returns `None` when absent, allowing a deliberate, clearer validation error. Missing and explicit `None` are both invalid amounts here. Do not use `if not amount` to reject missing amounts: that would also reject valid zero.

Although `float(True)` is `1.0`, accepting a Boolean as money would hide a data error. Also, `float('nan')` and `float('inf')` succeed. The added `math.isfinite()` check rejects those non-finite results before they contaminate an average.

Verified messages from the practical:

```text
ValueError: Transaction row 1 has an invalid amount; use a number.
ValueError: Transaction row 1 must have a non-empty category.
ValueError: Transaction row 1 must have a valid amount.
ValueError: Transaction row 1 amount must be finite.
```

Row numbers start at 1 among data records; they are not necessarily physical JSON or CSV line numbers. Extra fields are preserved, input records are not modified, categories are trimmed and lowercased, and finite negative amounts remain allowed.

## 9. Logging without secrets

`print()` presents the report to the user. Logging records operational events that help explain what happened. The toolkit answers three questions: did loading start, did it succeed or fail, and did the attempt finish?

```powershell
python -m data_toolkit.cli samples/transactions.json --verbose
```

The logs have this form (the run ID changes each time):

```json
{"event": "load_started", "run_id": "example", "entry_point": "cli"}
{"event": "load_succeeded", "run_id": "example", "entry_point": "cli", "record_count": 3}
{"event": "load_attempt_finished", "run_id": "example", "entry_point": "cli"}
```

These are illustrative IDs; the verification transcript contains actual run IDs. A failed load emits `load_failed` with an `error_type`, such as `FileNotFoundError`. Log messages are JSON objects so their fields are easy to identify. A run ID connects events from the same CLI invocation.

The implementation uses the standard library:

```python
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
logger.info('Loading started')
```

The real CLI wraps allowlisted metadata in `json.dumps()` before logging. No logging package or custom class is needed.

| Level | Purpose |
|---|---|
| `DEBUG` | Detailed investigation, usually disabled |
| `INFO` | Normal progress |
| `WARNING` | A handled problem that deserves attention |
| `ERROR` | A serious failure |
| `CRITICAL` | A failure threatening the whole application |

The CLI's expected bad-input errors use `WARNING`; progress uses `INFO` and appears with `--verbose`. Without that flag, successful Day 4 runs have no log output. Logs go to standard error; the summary goes to standard output. `finally` records completion of the load attempt, even when `parser.error()` exits.

Never log passwords, tokens, whole records, environment-variable contents or private transaction identifiers. Here the logs omit paths and raw exception messages too. Console reports can still contain user-requested paths and category/duplicate summaries; treat those reports as potentially private. A synthetic `PRIVATE-TOKEN` marker in tests checks that invalid-input errors do not echo the value. It is not a real credential.

## 10. Type hints make intentions visible

```python
def process_amount(text: str) -> float | None:
    ...
```

`text: str` describes the expected argument. `-> float | None` describes the possible return values. A `list[float]` is a list of numbers; `dict[str, int]` maps text keys to integer values. `-> None` describes a function that does not return a useful result.

Hints help readers and development tools. Python does not enforce them automatically. Runtime checks still matter for files and user input. `process_amount('nan')` is a conversion demonstration, not complete business validation; the toolkit's normalizer performs the additional finite-number checks.

The toolkit already had useful hints, including `str | Path`, `list[dict]` and `float | None`. The new exercises use those same conventions. No separate static type checker was installed or run.

## 11. Use the debugger to inspect the cause

```powershell
python -m pdb day5_practicals.py
```

At the `(Pdb)` prompt:

```text
b day5_practicals.broken_average
c
p amounts
p len(amounts)
where
q
```

The verified session stopped in `broken_average()`. `p amounts` displayed `[]`, and `p len(amounts)` displayed `0`. `where` showed how the practical reached that function. This directly confirms the cause before changing code.

| Command | Meaning |
|---|---|
| `b function_name` | Break when execution reaches a function |
| `n` | Run the next line without stepping into its function calls |
| `s` | Step into a function call |
| `p expression` | Print an expression's value |
| `l` | List nearby source lines |
| `where` | Show the call stack |
| `c` | Continue to the next stop |
| `q` | Quit the debugger |

For your own temporary investigation, `breakpoint()` inside a function opens the debugger there during normal execution. Remove temporary breakpoints when finished. Inspect only safe sample values in shared sessions.

## 12. Targeted tests protect the fix

A small test follows arrange, act, assert: prepare the input, run the function, compare the result.

```python
from data_toolkit.reports import calculate_average

def test_empty_average():
    result = calculate_average([])
    assert result is None
```

Use `==` for numeric equality and `is None` for the absence of a result. To verify an exception without a testing framework:

```python
try:
    validate_non_negative(-1.0)
except ValueError:
    pass  # This exception is the expected result of this test.
else:
    raise AssertionError('Expected ValueError for a negative amount.')
```

The `else` is essential: without it, the test could pass even if no exception were raised. Do not run assertion tests with `python -O`, because optimization removes assertions.

Run only the new validation checks while investigating:

```powershell
python run_day5_tests.py test_day5.py
```

Then run the full suite:

```powershell
python run_day5_tests.py
```

Verified result: **24 test functions passed**, followed by the existing smoke script's **five assertions**. The test functions contain multiple scenarios, so this is not a count of individual inputs. Existing reader, transformer, report and duplicate-ID tests are included. CLI tests launch real subprocesses using `sys.executable`, capture outputs and use temporary input files that are cleaned up automatically. No `unittest`, custom test classes or external test dependency is used.

The non-finite and private-value tests were run before the fixes and failed for the expected reasons. They passed after the fixes. This is the red → green process: first prove the gap exists, then prove the change closes it. No existing tests were weakened.

## 13. Verification and debugging record

| Issue | Symptom | Root cause | Fix or learning outcome | Verification |
|---|---|---|---|---|
| Invalid number | `float('hello')` raises `ValueError` | Text does not describe a number | Specific handler; clear normalizer validation | Original demo, combined practical and CLI checks |
| Negative exercise amount | A prohibited value could be accepted | A rule needs an explicit check | `raise ValueError` in exercise validator | Both positive and negative branches executed |
| Empty average | `ZeroDivisionError` | Empty list has length 0 | Existing `None` guard preserved | Raw traceback, debugger, existing average tests |
| Missing file | `FileNotFoundError` | Requested sample is absent | Existing demo handles absence; CLI reports error | Demo and CLI return status 2 |
| Malformed JSON | Decoder fails at line 6, column 5 | Trailing comma in exercise fixture | Retain fixture; CLI explains location | Practical and malformed-JSON subprocess |
| Missing fields | Normalization cannot produce a valid transaction | ID, amount or category absent | Validate before reporting; identify row/field | Each required field omitted in tests |
| Boolean amount | Could be mistaken for 1 or 0 | Python converts Booleans to floats | Existing Boolean rejection preserved | Explicit `True` regression check |
| Non-finite amount | `nan` accepted and could contaminate reports | `float()` accepts non-finite representations | Added `isfinite()` check | Red test failed, then four non-finite inputs rejected |
| Private input in errors | Invalid amount and ID echoed in exception | Error interpolated raw values | Use row number; suppress conversion chain display | Red test failed, then error/CLI marker checks passed |
| No progress logging | Hard to tell which load stage completed | CLI had no operational event logging | Optional safe JSON events with run ID | Success/failure events and counts checked |
| Python unavailable to this session | `python` not found; venv launcher failed | Session PATH and venv's base interpreter unavailable | Use bundled Python 3.12.14 for verification | Interpreter version and all commands captured |

The final verification transcript records 14 command runs, including expected nonzero exits for deliberate failures. An expected error is a successful exercise when its type, message and exit status match the check. The original sample files were retained. Existing Day 4 JSON and CSV runs still report:

```text
Transaction count: 3
Average amount: 75.0
Category counts: {'food': 2, 'transport': 1}
Duplicate IDs: set()
```

## 14. Recap and practice questions

Use this process: **reproduce → read the traceback → inspect the input → identify the root cause → fix → run the focused test → run the full suite**.

1. Why does `else` belong after `except`? It separates successful processing from error handling.
2. Does `finally` imply success? No; it runs when leaving the statement on both paths.
3. Why return `None` for an empty average? There are no values from which to calculate an average.
4. Why reject `True` as an amount? Numeric conversion would hide a type mistake.
5. Why is successful `float()` conversion insufficient? It also accepts `nan` and infinity.
6. What should logs identify? The event and safe diagnostic metadata, not secret values.
7. Do type hints validate JSON input? No; runtime checks remain necessary.
8. Why run the Day 4 tests? A Day 5 fix must preserve working behavior.

For independent practice, change only disposable exercise inputs: try `'0'`, a missing ID, an empty category, and a valid one-record JSON list. Predict each result before running it. Keep the deliberate broken function confined to this exercise.

