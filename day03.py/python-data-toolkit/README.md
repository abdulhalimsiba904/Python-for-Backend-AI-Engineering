# Python Data Toolkit

A beginner Python project demonstrating reusable functions, modules, imports, type hints, and basic data processing.

## Features

- Calculate the average of transaction amounts.
- Count transactions by category.
- Identify duplicate transaction IDs.
- Handle empty input when calculating averages.
- Run a demonstration through a command-line interface.
- Test functions using Python assertions.

## Project Structure

```text
python-data-toolkit/
├── src/
│   └── data_toolkit/
│       ├── __init__.py
│       ├── cli.py
│       ├── readers.py
│       ├── reports.py
│       ├── transformers.py
│       └── validators.py
├── tests/
│   ├── test_reports.py
│   └── test_validators.py
├── samples/
├── output/
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.10 or later
- No third-party packages are currently required.

## Run the Application

From the project directory, configure the package path in PowerShell:

```powershell
$env:PYTHONPATH = "src"
```

Run the application:

```powershell
python -m data_toolkit.cli
```

## Run the Tests

Run the report tests:

```powershell
python tests/test_reports.py
```

Run the duplicate-ID tests:

```powershell
python tests/test_validators.py
```

Run the original demonstration tests:

```powershell
python test_toolkit.py
```

## Learning Objectives

This project was built to practise Python functions, parameters, return values, type annotations, modules, imports, dictionaries, sets, list comprehensions, and basic testing.

## Project Status

Initial learning project. The toolkit currently uses sample transaction data and does not yet read external files.
