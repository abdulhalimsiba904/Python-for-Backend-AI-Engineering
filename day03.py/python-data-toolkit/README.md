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
