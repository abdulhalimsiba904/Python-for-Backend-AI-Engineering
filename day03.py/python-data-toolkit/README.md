# Python Data Toolkit

A Python 3.12 learning project for validating transaction CSV/JSON, computing
statistics, exporting reports, and optionally producing structured document
summaries. Default summary mode is deterministic and offline. Runtime uses only
Python's standard library; pytest is a development dependency.

This application lives inside `day03.py/python-data-toolkit` in the larger Python
for Backend & AI Engineering repository. Commands below run **from this application
folder**, not the repository root. The application is run from its `src` layout;
it is not currently packaged for `pip install -e .`.

## Features and contracts

- Explicit transaction commands: `validate`, `analyze`, `convert`, `report`.
- CSV numeric-string conversion and historical `id` adaptation; JSON amounts remain
  strictly numeric. Positive finite amounts only; booleans are rejected.
- Duplicate transaction IDs are detected after trimming. Duplicate CSV header names
  are rejected before ambiguous columns can overwrite one another.
- Canonical output trims IDs, normalizes category whitespace/case and converts
  amounts to floats. Extra metadata is omitted from canonical Day 10 output.
- Reports include count, total, rounded average, extrema and category counts/totals.
- Atomic file publication protects inputs and refuses overwrites unless `--force`
  is explicitly supplied. Original source files remain unchanged.
- `summarize` accepts UTF-8 text with mock or opt-in GroqCloud providers, strict
  application validation, safe failures and an explicit `--fallback` option.
- Earlier direct-file/no-argument transaction commands remain available. Their
  legacy normalization rules are separate from the canonical Day 10 commands.

## Fresh Windows PowerShell setup

Prerequisites: Windows 11, Git, Python 3.12 with its `py` launcher, and optionally
VS Code with the Python extension. Use a new folder for the clone, especially if
your existing repository contains unfinished changes or private practical notes.

```powershell
git clone https://github.com/abdulhalimsiba904/Python-for-Backend-AI-Engineering.git PythonDataToolkit-review
Set-Location '.\PythonDataToolkit-review\day03.py\python-data-toolkit'
py -3.12 -m venv .venv
$toolkitPython = Join-Path $PWD '.venv\Scripts\python.exe'
& $toolkitPython -m pip install -r requirements-dev.lock
$env:PYTHONPATH = (Join-Path $PWD 'src')
& $toolkitPython --version
& $toolkitPython -m pip check
```

The clone command obtains the published default branch. Until Day 13 is approved
and published, use the supplied review patch on a clean copy at base commit
`eb00ff8e77c508472340e91f45ff8968c5e70ec0` to obtain these changes. A new clone of
GitHub alone does not contain uncommitted Day 13 files.

The lock file records the existing pytest dependency and its resolved transitive
versions for Windows/Python 3.12; it adds no runtime dependency. It is a version
snapshot, not a hash-verified supply-chain guarantee. `requirements-dev.txt` remains
the original flexible developer specification. Do not regenerate the lock from a
global environment containing unrelated packages. Refresh it deliberately and retest.
No packages are needed to run the offline CLI if testing tools are not required.

Using the explicit executable avoids PowerShell activation-policy changes. In VS
Code select this `.venv\Scripts\python.exe` using **Python: Select Interpreter**.
If `py` is unavailable, use the full path to a working Python 3.12 interpreter to
create the environment. Do not reuse a venv referencing a removed interpreter.

## CLI reference

```powershell
& $toolkitPython -m data_toolkit.cli --help
& $toolkitPython -m data_toolkit.cli report --help
& $toolkitPython -m data_toolkit.cli summarize --help
```

The top-level help describes transaction commands; summary options are shown by
`summarize --help`. All documented subcommands exist in the inspected CLI.

| Command | Purpose | Required output option |
|---|---|---|
| `validate FILE` | Reject an entire invalid batch or print valid/count JSON | None |
| `analyze FILE` | Print canonical statistical JSON | None |
| `convert FILE --output FILE.json` | Export canonical JSON | `.json` destination |
| `report FILE --output FILE.txt` | Export a readable report | `.txt` destination |
| `summarize FILE.txt` | Print a four-field summary; default mock | None |

### Transaction examples and expected results

```powershell
& $toolkitPython -m data_toolkit.cli validate samples/transactions.csv
& $toolkitPython -m data_toolkit.cli analyze samples/transactions.csv
```

Validation returns `{"valid": true, "count": 3}` (formatted as indented JSON).
Analysis of that fixture has count 3, total 225.0, average 75.0, minimum 50.0,
maximum 100.0; food has count 2/total 175.0 and transport count 1/total 50.0.
Required CSV fields are `id` (or `transaction_id`), `amount`, and `category`.

Create fresh output files with the default no-overwrite path:

```powershell
& $toolkitPython -m data_toolkit.cli convert samples/transactions.csv --output output/day13-converted.json
& $toolkitPython -m data_toolkit.cli report samples/transactions.csv --output output/day13-report.txt
```

These return JSON acknowledgements after successful publication. The parent
directory is created if needed. A report from the fixture matches
[`samples/day13_expected_report.txt`](samples/day13_expected_report.txt). If a
destination already exists, review it before deliberately adding `--force` to
replace it. Input and output must differ, including aliases to the same file.
Never use `--force` merely to bypass an error you have not understood.

Earlier invocation forms remain valid:

```powershell
& $toolkitPython -m data_toolkit.cli
& $toolkitPython -m data_toolkit.cli samples/transactions.json
& $toolkitPython -m data_toolkit.cli samples/transactions.csv --verbose
```

They print the legacy report to the terminal. Extra metadata preservation in the
legacy normalizer is not a promise about canonical `convert` output.

### Invalid inputs are expected failures

```powershell
& $toolkitPython -m data_toolkit.cli validate samples/day10_invalid.csv
& $toolkitPython -m data_toolkit.cli validate samples/day13_duplicate_headers.csv
```

Both return exit 1. The first identifies existing duplicate-ID/nonpositive-amount
rules. The second returns `error: CSV header contains duplicate field names.`
Missing files, malformed JSON and invalid data also fail safely. No report should
be published from an invalid batch. Exit 0 means success/help, exit 1 an expected
processing/configuration failure, and exit 2 invalid CLI usage. Legacy errors use
argparse conventions and can return exit 2 for input failures too.

## Offline document summaries

```powershell
& $toolkitPython -m data_toolkit.cli summarize samples/day11_operations.txt
```

Expected title: `Quarterly Operations Report`. The mock joins the nonblank lines
into a bounded summary, takes up to three following lines as key points and returns
`open_questions: []`. It extracts text deterministically and is not an AI reasoning
system. Merely setting an API key never changes this default.

The result has exactly `title: str`, `summary: str`, `key_points: list[str]` and
`open_questions: list[str]`. Title/summary bounds are 200/2000 characters; key points
require 1–10 nonblank strings, open questions allow 0–10, and each item is <=500
characters. Input is nonblank UTF-8 text of at most 20000 characters. JSON syntax,
schema validity and factual correctness are separate requirements; human source
review is still necessary for a real AI summary.

## Optional Groq configuration and costs

No key is needed for tests or mock summaries. To opt into live mode later, obtain
your own GroqCloud key and enter it privately in your local PowerShell terminal:

```powershell
$groqKeyInput = Read-Host 'Groq API key (hidden)' -AsSecureString
$env:GROQ_API_KEY = [System.Net.NetworkCredential]::new('', $groqKeyInput).Password
Remove-Variable groqKeyInput
$env:GROQ_MODEL = 'openai/gpt-oss-20b'
```

**Optional live command — not executed during Day 13 verification:**

```powershell
& $toolkitPython -m data_toolkit.cli summarize samples/day11_operations.txt --provider groq --timeout 30
```

This sends document content externally and may incur charges. Check your account's
model access, current pricing, quota, rate limits and available spend controls.
Only send documents you are authorized to disclose. Groq reads `GROQ_API_KEY` only;
optional `GROQ_MODEL` defaults to `openai/gpt-oss-20b`. The publisher prefix does not
select the OpenAI API. A replacement model must support Groq strict JSON Schema.
The adapter uses Groq's HTTPS Chat Completions endpoint with an explicit User-Agent,
one attempt, a 2048-token completion cap, response bounds and no redirects/retries.

`--timeout` defaults to 15 and must be finite, >0 and <=120 seconds. It bounds socket
operations rather than guaranteeing a total elapsed deadline. A timeout may occur
after a request has already been processed. Add `--fallback` only when you explicitly
want a mock result on provider/response failure; stdout remains four-field JSON
and stderr identifies fallback. Input/timeout errors are still rejected first.

Clear session values after live use:

```powershell
Remove-Item Env:GROQ_API_KEY -ErrorAction SilentlyContinue
Remove-Item Env:GROQ_MODEL -ErrorAction SilentlyContinue
```

Never hardcode, print, log or commit actual keys. Keep them out of frontend code,
tests, documents, screenshots and chat. Environment variables are plaintext while
in use. `.env` files are ignored, but **this application does not load them**.
An ignore rule cannot untrack a previously committed secret. Rotate exposed keys
at the provider; deleting a local file does not invalidate them.

## Testing and optional quality tools

Run from this application directory with the same interpreter used for installation:

```powershell
& $toolkitPython -m pytest -q
& $toolkitPython -m pytest -q tests/day11
& $toolkitPython -m unittest discover -s tests/day12 -p 'test_*.py' -v
& $toolkitPython -m unittest discover -s tests/day13 -p 'test_*.py' -v
```

Pytest is the complete runner: it collects pytest functions, unittest cases and
earlier smoke assertions using `pytest.ini`. The old `run_day5_tests.py` covers only
the historical root tests and is **not** the complete regression suite. Tests use
temporary fixtures and local fake API responses, not real keys or API credits.

Optional development-only static tools, using versions exercised during Day 13:

```powershell
& $toolkitPython -m pip install 'ruff==0.17.3' 'mypy==2.4.1'
& $toolkitPython -m ruff check --no-cache --select E4,E7,E9,F src tests day07_assessment test_toolkit.py
& $toolkitPython -m mypy --check-untyped-defs --no-incremental src
& $toolkitPython -m pip check
```

Ruff checks the selected correctness rules, not every style rule. Mypy checks the
existing annotation coverage and untyped bodies; it is not a strict full-typing
claim. Neither tool replaces running workflows. The dependency check is not a
security-advisory audit. Detailed observed commands/results and environment limits
are recorded in [`docs/DAY13_QUALITY_REPORT.md`](docs/DAY13_QUALITY_REPORT.md).

## Architecture and repository layout

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the Mermaid data-flow diagram,
legacy path, provider boundary and file-publication guarantees.

```text
python-data-toolkit/
  src/data_toolkit/       CLI, file adapters, models and summary providers
    day09/               validation, transformation and statistics
  tests/                 earlier tests plus day08 through day13 suites
  day07_assessment/      earlier unittest learning exercises
  samples/               public success/error fixtures and expected output
  docs/                  architecture, debugging and verification evidence
  output/                generated exports; existing tracked examples remain
  requirements.txt       empty: standard-library runtime
  requirements-dev.txt   flexible existing pytest requirement
  requirements-dev.lock  resolved Windows/Python 3.12 test environment
  pytest.ini             complete test discovery and source paths
```

Earlier standalone scripts are legitimate learning artifacts, not cleanup targets.
`.gitignore` covers environments, caches, logs, generated outputs and private notes;
Day 13 adds mypy/Ruff cache rules without removing existing protections. Two
historical exports are already tracked; ignore rules do not hide tracked files.
Inspect `git status --short` and review exact paths before staging changes.

## Troubleshooting and limitations

| Symptom | Investigation |
|---|---|
| `No module named data_toolkit` | Check working directory and set `PYTHONPATH` to the absolute `src` folder. |
| Missing Python or broken venv | Use a working Python 3.12 to create a new environment; do not copy a venv between machines. |
| Missing pytest | Install the development requirements with the exact interpreter you run. |
| `--output` required / exit 2 | Check subcommand help and argument spelling. |
| Existing destination | Inspect the file; choose another name or deliberately use `--force`. |
| Hard-link publication denied | Test filesystem permissions/capabilities; do not weaken the exporter to hide an environment failure. |
| Duplicate CSV headers | Correct the source schema; repeated names are ambiguous and now rejected. |
| Provider configuration / 401 / 403 | Check key presence locally and Groq model/project permissions; never print credentials. |
| 429 / unavailable service / timeout | Check limits/connectivity and deliberately retry later or choose fallback. |
| Valid JSON with wrong claims | Compare schema and facts against the original document. |

This is a learning toolkit, not a packaged web service. It does not parse PDF/Word
documents, chunk long text, guarantee AI facts, provide total request deadlines or
make automatic retries. It uses floats, not financial-grade decimal accounting.
Potential later work includes packaging and CI, after preserving the tested public
contracts. Day 14 preparation should focus on an independent demonstration and
explaining the code; Phase 2 database work has not begun.

Contributions should reproduce a defect with a test, make a small justified change,
run the full suite/static checks, and document observed results. Review each staged
path, protect private files and obtain project-owner approval before publishing or
merging. Day 13 is prepared on `day13-documentation-repository-quality`;
merging that feature branch into main requires separate owner approval.
