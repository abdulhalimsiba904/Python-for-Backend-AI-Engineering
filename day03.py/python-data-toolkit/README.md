# Python Data Toolkit

A beginner Python project for reading transaction data from JSON and CSV files, normalizing records, validating transaction fields, and generating summary reports.

## Features

- Read transaction data from JSON and CSV files.
- Normalize transaction IDs, amounts, and categories.
- Calculate the average transaction amount.
- Count transactions by category.
- Detect duplicate transaction IDs.
- Report errors for missing files, unsupported file formats, malformed JSON, and invalid transaction data.
- Preserve additional transaction fields during normalization.

## Project Structure

```text
python-data-toolkit/
├── output/
├── samples/
├── src/
│   └── data_toolkit/
│       ├── __init__.py
│       ├── cli.py
│       ├── readers.py
│       ├── reports.py
│       ├── transformers.py
│       └── validators.py
└── tests/
    ├── test_readers.py
    ├── test_transformers.py
    ├── test_reports.py
    └── test_validators.py
```

## Requirements

- Python 3.12 or a compatible Python version.
- No third-party packages are currently required.

## Running the Toolkit

Open a terminal in the project root.

On Windows PowerShell, configure Python to find the `src` directory:

```powershell
$env:PYTHONPATH = "src"
```

Run the toolkit using the sample JSON file:

```powershell
python -m data_toolkit.cli
```

Run it with a specific JSON or CSV file:

```powershell
python -m data_toolkit.cli samples/transactions.json
python -m data_toolkit.cli samples/transactions.csv
```

The default input file is `samples/transactions.json`.

## Running Tests

Run the complete suite from the toolkit project folder, even in a fresh
terminal without setting `PYTHONPATH`:

```powershell
python run_day5_tests.py
python run_day5_tests.py test_day5.py
```

The runner locates `src` automatically. It runs the original reader,
transformer, report and duplicate-ID tests, the smoke checks, and the Day 5
validation, logging, CLI and runner regression tests. Tests use functions and
plain assertions; no third-party test framework is required.

Run the test scripts individually:

```powershell
python tests/test_readers.py
python tests/test_transformers.py
python tests/test_reports.py
python tests/test_validators.py
```

Each test script uses Python assertions to check expected behavior.
The individual scripts and application commands still use the `PYTHONPATH`
setting shown above.

## Sample Output

```text
=== Python Data Toolkit ===
Input file: samples/transactions.json
Transaction count: 3
Average amount: 75.0
Category counts: {'food': 2, 'transport': 1}
Duplicate IDs: set()
```

## Learning Objectives

This project practices Python functions, modules, type hints, file handling, JSON and CSV processing, path management, data validation, exception handling, command-line arguments, and basic testing.

## Day 5: Exceptions and Debugging

Read [the full Day 5 lesson](DAY5_LESSON.md) for the three-hour curriculum,
debugging issue log, commands, explanations and verified outputs.

```powershell
$env:PYTHONPATH = 'src'
python day5_practicals.py
python run_day5_tests.py test_day5.py
python run_day5_tests.py
python -m data_toolkit.cli samples/transactions.json --verbose
python -m pdb day5_practicals.py
```

`--verbose` shows safe progress logs on standard error. Expected load failures
produce a warning and an actionable error; successful default reports retain
their Day 4 output. Amount validation rejects Booleans and non-finite numbers,
keeps zero and finite negative refunds, and reports record numbers instead of
echoing private IDs or invalid values. No additional dependencies are required.

The practicals cover `try`/`except`/`else`/`finally`, deliberate `raise`,
traceback investigation and debugger inspection. Type hints document expected
inputs and results, including `float | None`; runtime checks still validate
external data. The full lesson includes symptom, root cause, fix and
verification notes for the debugging exercises.

## Day 6: Object-Oriented Programming, Git, and Clean Code

`DocumentRecord` keeps one input document's identity, filename, format, status,
and independent validation-error list together. Methods demonstrate initialization,
instance state, and controlled status changes. Readers, transformations,
validators, and reports remain functions; there is no inheritance hierarchy.

New files include `src/data_toolkit/models.py`,
`src/data_toolkit/processing.py`, `document_record_demo.py`,
`tests/test_models.py`, and `tests/test_processing.py`.

The record accepts PDF, CSV, JSON, and TXT **metadata**; the transaction pipeline
still reads JSON and CSV only. Normal status progression is pending, processing,
completed. A recorded error makes the record failed. Create a new record for a
retry. Caller-supplied identifiers must be nonblank strings; callers manage
uniqueness, and the integration demo uses UUIDs.

```python
from data_toolkit.models import DocumentRecord

record = DocumentRecord("DOC-001", "transactions.json", "json")
record.mark_processing()
record.mark_completed()
print(record.get_summary())
# DOC-001 | transactions.json | JSON | completed | errors: 0
```

That example demonstrates the lifecycle only; it does not open a file. The demo
also calls `process_document(record, path)` to read and normalize actual JSON/CSV
samples with the existing toolkit functions, then calculate reports. Expected
input errors mark the record failed with a safe stored message and re-raise the
original exception. The existing CLI keeps its arguments, report text, and logging.

From the toolkit folder in PowerShell:

```powershell
python document_record_demo.py
python run_day5_tests.py test_models.py
python run_day5_tests.py test_processing.py
python run_day5_tests.py
$env:PYTHONPATH = 'src'
python -m data_toolkit.cli samples/transactions.json
python -m data_toolkit.cli samples/transactions.csv
```

The demo finds `src` itself, as does the existing test runner. The full suite now
runs **50 test functions plus 5 original smoke checks**. It includes exact CLI
output checks and all previous regression tests. No new dependencies are needed.

If `python` is unavailable in your terminal, the verification session used:

```powershell
$py = 'C:\Users\USER\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $py --version  # Python 3.12.14 in the verification session
& $py document_record_demo.py
& $py run_day5_tests.py
```

Use `& $py` in place of `python` in the other commands when necessary. Python
3.12.10 was not available to this execution session; no local environment was
recreated. See [Day 6 design decisions](DAY6_DESIGN_DECISIONS.md) and
[Day 6 practical notes](DAY6_PRACTICAL_NOTES.md) for the lifecycle rules,
encapsulation limits, implementation details, actual results, and Git workflow.

Day 6 work stays on `feature/day6-oop-clean-code` as local commits. Review staged
diffs and stage exact filenames. Do not include secrets, generated output, local
environments, or the unrelated `rc` file. Pushing or merging requires approval.
