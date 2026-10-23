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

Run the test scripts individually:

```powershell
python tests/test_readers.py
python tests/test_transformers.py
python tests/test_reports.py
python tests/test_validators.py
```

Each test script uses Python assertions to check expected behavior.

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
