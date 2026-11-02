# Python for Backend & AI Engineering

A practical record of my progress through **Phase 1: Python and Software Engineering Foundations** of a Full-Stack AI Engineering learning roadmap.

I am **Abdul Halim Siba**, a Computer Science student at the University for Development Studies (UDS), Ghana, and a developing Full-Stack AI Engineer. I am learning Python to build a foundation for backend systems and AI-enabled applications, with an emphasis on hands-on implementation, debugging, testing, documentation, and maintainable code.

**Progress:** Days 1–13 completed. **Day 14 — Final Assessment and Project Demonstration is upcoming.** This repository contains learning exercises and a growing command-line application; database and web API development are future phases.

[Learning progress](#learning-progress) · [Featured project](#featured-project--python-data-toolkit) · [Getting started](#getting-started) · [Testing](#testing-and-quality-assurance) · [Roadmap](#roadmap-and-next-steps)

## Learning objectives

The work in this repository demonstrates:

- Python syntax, variables, types, input conversion, and conditional logic.
- Loops, lists, dictionaries, filtering, sorting, and duplicate detection.
- Functions, imports, modules, packages, and reusable processing code.
- Text, CSV, and JSON file handling and structured transaction processing.
- Validation, exception handling, safe diagnostic logging, and debugging.
- Object-oriented modeling of document metadata and processing state.
- Automated tests, integration tests, and regression prevention.
- Separation of CLI interaction, application logic, file handling, and provider-specific code.
- Git-based incremental development, technical documentation, and reproducible test environments.

These are foundations for my broader goal of building backend and AI systems. They do not imply that this repository already implements a database, REST service, or full-stack application.

## Learning progress

Days are learning milestones, not separate standalone applications. From Day 4 onward, much of the work extends the Python Data Toolkit inside the historically named `day03.py/` directory.

| Day | Topic / focus | Practical work and evidence | Status |
|---|---|---|---|
| 1 | Python basics and data types | [Foundations scripts](day01/): variables, type inspection, console output, and an interactive personal profile with explicit yes/no handling. | Completed |
| 2 | Control flow and data structures | [Transaction exercises](day02/): totals, category counts, duplicate IDs, filtering, and sorting using lists, dictionaries, and loops. | Completed |
| 3 | Functions and modules | [Calculation functions](day03.py/calculations.py) imported by [main.py](day03.py/main.py) to compute totals and averages. | Completed |
| 4 | File handling and structured data | Toolkit [text](day03.py/python-data-toolkit/read_text.py), [CSV](day03.py/python-data-toolkit/read_csv.py), and [JSON](day03.py/python-data-toolkit/read_json.py) exercises, corresponding write scripts, and reusable [readers](day03.py/python-data-toolkit/src/data_toolkit/readers.py). | Completed |
| 5 | Exceptions, debugging, logging, and type hints | [Practical script](day03.py/python-data-toolkit/day5_practicals.py), exception/debugging demonstrations, and [automated checks](day03.py/python-data-toolkit/tests/test_day5.py). | Completed |
| 6 | OOP and code organization | [DocumentRecord](day03.py/python-data-toolkit/src/data_toolkit/models.py) models metadata, status transitions, and validation errors; [model tests](day03.py/python-data-toolkit/tests/test_models.py) check behavior. | Completed |
| 7 | Foundations assessment | [Three assessment exercises](day03.py/python-data-toolkit/day07_assessment/README.md): student statistics, a safe JSON reader, and transaction category analysis, with unittest cases. | Completed |
| 8 | Automated testing with pytest | [pytest suites](day03.py/python-data-toolkit/tests/day08/) cover files, reports, and transactions using fixtures and temporary data. | Completed |
| 9 | Validation, transformation, and statistics | [Day 9 package](day03.py/python-data-toolkit/src/data_toolkit/day09/) separates transaction validation, normalization, and statistical calculations. | Completed |
| 10 | CLI and application architecture | [Command orchestration](day03.py/python-data-toolkit/src/data_toolkit/day10_cli.py) and [application functions](day03.py/python-data-toolkit/src/data_toolkit/application.py) support validation, analysis, conversion, and reports. | Completed |
| 11 | AI API integration and structured summaries | [Provider-independent summary service](day03.py/python-data-toolkit/src/data_toolkit/summaries.py), deterministic offline mock, optional [Groq adapter](day03.py/python-data-toolkit/src/data_toolkit/groq_summary.py), and [mocked provider tests](day03.py/python-data-toolkit/tests/day11/). | Completed |
| 12 | Integration testing, refactoring, and typing | [Reporting workflow tests](day03.py/python-data-toolkit/tests/day12/test_reporting_workflow.py) exercise public workflows; [quality report](day03.py/python-data-toolkit/DAY12_QUALITY_REPORT.md) records the work and its verification limits. | Completed |
| 13 | Documentation, repository quality, and debugging | [Architecture documentation](day03.py/python-data-toolkit/docs/ARCHITECTURE.md), dependency snapshot, and [three duplicate CSV-header regression tests](day03.py/python-data-toolkit/tests/day13/test_csv_headers.py). | Completed |
| 14 | Final assessment and project demonstration | Independently demonstrate the project and explain its design, tests, and limitations. | **Upcoming** |

## Featured project — Python Data Toolkit

**[Read the Python Data Toolkit guide →](day03.py/python-data-toolkit/README.md)**

The toolkit brings the exercises together into a modular command-line application. It demonstrates backend fundamentals through input validation, predictable data processing, reusable application functions, and tested error paths.

Verified capabilities include:

- Read transaction CSV and JSON; adapt supported historical input fields.
- Validate required fields, positive finite amounts, and duplicate transaction IDs; reject duplicate CSV headers before values can be overwritten.
- Normalize transaction IDs and categories and calculate totals, averages, extrema, and category statistics.
- Run `validate`, `analyze`, `convert`, and `report` commands, while preserving earlier invocation forms.
- Export canonical JSON and text reports with same-file checks and explicit overwrite protection.
- Summarize UTF-8 text using a deterministic offline mock or an explicitly selected GroqCloud provider.
- Validate summary JSON against four fields: `title`, `summary`, `key_points`, and `open_questions`; offer explicit mock fallback on provider failure.

The mock performs deterministic text extraction; it is not an AI model. A real provider sends document content externally and requires credentials, model access, and attention to cost and rate limits. Valid JSON and a valid schema do not establish factual correctness.

The application uses Python's standard library at runtime. It is a learning CLI, not a deployed backend service. It does not parse PDF/Word files, guarantee AI accuracy, or provide financial-grade decimal accounting.

Explore the [architecture explanation](day03.py/python-data-toolkit/docs/ARCHITECTURE.md), [editable Mermaid source](day03.py/python-data-toolkit/docs/architecture.mmd), and [Day 13 verification record](day03.py/python-data-toolkit/docs/DAY13_QUALITY_REPORT.md).

## Repository structure

Selected tracked paths are shown below; repetitive scripts, fixtures, and tests are omitted. Private notes, local environments, and caches are not part of this overview.

```text
Python-for-Backend-AI-Engineering/
├── README.md
├── .gitignore
├── day01/
│   ├── hello.py
│   ├── variables.py
│   ├── data_types.py
│   └── personal_profile.py
├── day02/
│   ├── transaction_checker.py
│   └── transaction_processor.py
└── day03.py/
    ├── calculations.py
    ├── main.py
    └── python-data-toolkit/
        ├── README.md
        ├── DAY12_QUALITY_REPORT.md
        ├── day07_assessment/
        ├── docs/
        │   ├── ARCHITECTURE.md
        │   ├── architecture.mmd
        │   └── DAY13_QUALITY_REPORT.md
        ├── samples/
        ├── output/
        ├── src/data_toolkit/
        │   ├── cli.py
        │   ├── application.py
        │   ├── models.py
        │   ├── readers.py
        │   ├── day09/
        │   ├── day10_cli.py
        │   ├── day11_cli.py
        │   ├── summaries.py
        │   └── groq_summary.py
        ├── tests/
        │   ├── day08/ … day13/
        │   └── test_*.py
        ├── pytest.ini
        ├── requirements.txt
        ├── requirements-dev.txt
        └── requirements-dev.lock
```

`day03.py` is a directory despite its suffix. Earlier standalone file-handling and debugging scripts remain inside the toolkit directory. `output/` contains two historical tracked exports; newly generated outputs are ignored.

## Technologies and tools

| Area | Used in this repository |
|---|---|
| Language | Python; documented clean-environment verification uses Python 3.12. |
| Runtime libraries | Standard-library modules including `csv`, `json`, `argparse`, `pathlib`, `logging`, `urllib.request`, and `unittest`. |
| Testing | pytest, unittest, temporary fixtures, and mocked external responses. |
| Development environment | Windows PowerShell, VS Code, and Python virtual environments. |
| Version control | Git and GitHub, with incremental commits and reviewed feature branches. |
| Documentation and quality | Markdown, Mermaid architecture diagrams, and recorded Ruff/mypy checks. |
| Optional external integration | GroqCloud over HTTPS; offline mock is the default. |

SQL, PostgreSQL, relational modeling, REST API development, and full-stack application frameworks belong to later learning phases.

## Getting started

### Prerequisites

Use Git, Python 3.12 with the Windows `py` launcher, and Windows PowerShell. VS Code with its Python extension is optional. Use a fresh clone location rather than overwriting an existing checkout or virtual environment.

### Clone and prepare the toolkit

```powershell
git clone https://github.com/abdulhalimsiba904/Python-for-Backend-AI-Engineering.git
Set-Location '.\Python-for-Backend-AI-Engineering\day03.py\python-data-toolkit'
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.lock
$env:PYTHONPATH = (Join-Path $PWD 'src')
```

Run all remaining commands **from `day03.py/python-data-toolkit`**. The application uses a `src` layout and is not packaged for `pip install -e .`. `PYTHONPATH` is needed for CLI execution in each new terminal session; pytest configures its own source paths.

If PowerShell blocks activation, use the virtual environment's executable directly without changing execution policy:

```powershell
& .\.venv\Scripts\python.exe -m pip install -r requirements-dev.lock
$env:PYTHONPATH = (Join-Path $PWD 'src')
& .\.venv\Scripts\python.exe -m data_toolkit.cli validate samples/transactions.csv
```

For the `python` commands below, activate the environment or substitute that explicit executable. In VS Code, select `.venv\Scripts\python.exe` through **Python: Select Interpreter**.

`requirements-dev.lock` pins pytest and its resolved dependencies for the documented Windows/Python 3.12 environment. It is a version snapshot without package hashes. The runtime requirements file is empty; installing development dependencies enables testing, not the offline application itself.

### Run the application

```powershell
python -m data_toolkit.cli --help
python -m data_toolkit.cli validate samples/transactions.csv
python -m data_toolkit.cli analyze samples/transactions.csv
python -m data_toolkit.cli summarize samples/day11_operations.txt --provider mock
```

The transaction sample contains three records with total `225.0` and average `75.0`. The summary command runs locally without an API key or API charges. Use `summarize --help` for summary-specific options.

To create output files, choose destinations that do not already exist:

```powershell
python -m data_toolkit.cli convert samples/transactions.csv --output output/converted.json
python -m data_toolkit.cli report samples/transactions.csv --output output/report.txt
```

Existing destinations are refused unless `--force` is deliberately supplied. Input and output must differ. See the [project guide](day03.py/python-data-toolkit/README.md#cli-reference) for legacy commands, errors, and detailed contracts.

### Run automated tests

```powershell
python -m pytest -q
python -m pytest -q tests/day13
```

The first command runs the complete configured suite, including the Day 7 assessment, earlier tests, and later regression suites. The second targets the three Day 13 cases. Tests use local fixtures and mocked provider responses; no real API key, internet access, or API credits are required after dependencies are installed.

For optional live Groq setup, follow the [credential and cost instructions](day03.py/python-data-toolkit/README.md#optional-groq-configuration-and-costs). Keep real keys out of source code, frontend code, tests, documentation, and Git. `.env` files are ignored but are not automatically loaded by this application. Selecting `--provider groq` is explicit; setting a key alone does not change the default mock provider.

## Testing and quality assurance

The [Day 13 quality report](day03.py/python-data-toolkit/docs/DAY13_QUALITY_REPORT.md#final-test-and-static-results) records **326 passing tests and 14 additional passing subtests**, with zero failures or skips, in a newly created Windows/Python 3.12 virtual environment. These are recorded verification results, not a live CI badge or a guarantee for every machine.

Three Day 13 regression tests cover duplicate CSV-header rejection, safe CLI failure without publishing a report, and preserved behavior for unique headers. This prevents `csv.DictReader` from silently replacing an earlier column value when header names repeat.

The suite combines pytest functions, unittest cases, integration workflows, and earlier smoke assertions. It checks valid and invalid inputs, file publication, CLI behavior, and mocked provider failures. The old Day 5 runner is a historical subset rather than the full regression command.

The report also records selected Ruff checks, mypy checks over 18 source files, and dependency consistency checks. Those tools are optional development tools and are not installed by the test lock file. The report is a historical pre-publication record; its branch-state statements describe that earlier snapshot. Git history establishes subsequent publication.

## Engineering practices

- **Defined responsibilities:** CLI routing, application orchestration, readers, business functions, and summary providers live in separate modules.
- **Validation at boundaries:** Transaction batches and provider output are checked before use; malformed inputs produce meaningful failures.
- **Regression prevention:** Defects receive focused tests, followed by complete-suite verification.
- **Controlled file output:** Same-file and overwrite guards protect source data; temporary files support atomic publication on compatible filesystems.
- **Reproducible development:** A test dependency snapshot, documented working directory, and explicit import-path setup reduce environment ambiguity.
- **Incremental Git workflow:** Commit history records the progression from basic scripts to integration testing and documentation improvements.
- **Evidence-based documentation:** Architecture and quality reports explain contracts, observed results, and remaining limitations.

## Roadmap and next steps

| Stage | Status and direction |
|---|---|
| Phase 1, Days 1–13 | Completed practical foundations, toolkit development, testing, and documentation. |
| Day 14 | **Upcoming:** final assessment, independent project demonstration, and explanation of implementation decisions. |
| Phase 2 | Planned: SQL, PostgreSQL, and relational data modeling. |
| Later phases | Planned: REST APIs, backend systems, and broader AI integration toward full-stack applications. |

These next steps describe learning goals, not additional features already implemented here.

## Author

**Abdul Halim Siba**  
Computer Science Student | Software Builder | Developing Full-Stack AI Engineer  
University for Development Studies (UDS), Ghana

[GitHub](https://github.com/abdulhalimsiba904) · [LinkedIn](https://www.linkedin.com/in/abdul-halim-siba-2431b8440/)
