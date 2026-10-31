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
- Runtime: standard library only. Development tests: pytest (requirements-dev.txt).

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


## Day 8 Automated Testing with pytest

Run commands from `C:\Users\USER\python-foundations\day03.py\python-data-toolkit`.
Use a working Python 3.12 interpreter; do not delete an existing environment
if its original interpreter is missing. The optional `.venv-day8` below is separate.

```powershell
python -m venv .venv-day8
& .\.venv-day8\Scripts\python.exe -m pip install -r requirements-dev.txt
& .\.venv-day8\Scripts\python.exe -m pytest -q
& .\.venv-day8\Scripts\python.exe -m pytest tests/day08 -v
& .\.venv-day8\Scripts\python.exe -m pytest --collect-only -q
```

If `python` is not on PATH, use a verified full interpreter path with PowerShell's
`&` operator. For the bundled interpreter used in the Day 8 verification:

```powershell
$py = 'C:\Users\USER\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $py --version
# Prefer creating .venv-day8 with this interpreter, then use its python.exe above.
& $py -m venv .venv-day8
```

`pytest.ini` supplies `src` and `day07_assessment` import paths during tests.
The default suite includes all existing tests, Day 7 unittest tests and the
original top-level smoke script (its assertions execute during collection).
New pytest examples live under `tests/day08/` so the old no-dependency runner
does not try to call fixture-dependent tests. The old runner and Day 7 unittest
commands remain available. Run from this folder because older tests use relative
sample paths. New file tests use `tmp_path` and never alter sample files.

### Intended behavior before writing tests

- `calculate_average([2, 4, 6]) == 4`; empty numeric list returns `None`.
  Repeated numbers count separately; finite negative values and zero are valid;
  the result is rounded to two decimal places. String or None elements in a
  nonempty numeric list raise `TypeError`. This helper assumes numeric lists:
  it is not a full input validator and does not reject Booleans itself.
- Day 7 statistics count scores >= 50 as passing, retain repeated scores,
  return zero total/count/pass/fail and None average/min/max for an empty list,
  and do not change input. Mixed numeric/string elements raise `TypeError`.
  Score-range and Boolean validation are outside this helper's current contract.
- Transaction normalization requires nonblank string `id` and `category`, and
  an amount convertible to a finite float. Missing fields, invalid amounts,
  Booleans, NaN and infinity raise `ValueError`. Zero and refunds remain valid.
  Extra fields and duplicate records are retained. Duplicate detection reports
  repeated IDs as a set; it does not remove records. Input dictionaries are
  copied at the top level; nested extra values are not promised deep copies.
- Toolkit category counting expects normalized dictionaries with a category;
  a missing category raises `KeyError`. Day 7's independent counter instead
  skips missing, blank or non-string categories and normalizes case/outer spaces.
- Malformed or empty JSON text raises `json.JSONDecodeError`; valid JSON of
  the wrong shape raises `ValueError`; `[]` loads as an empty list. A missing
  file raises `FileNotFoundError`. CSV missing required fields is rejected by
  normalization. CSV parsing is not a strict detector of every malformed CSV.
- `process_document` re-raises malformed JSON and marks its record failed with
  a safe message. Successful JSON/CSV processing completes the record.

Function-scoped fixtures provide fresh transaction data. Parametrization names
independent cases; `pytest.raises` checks error conditions. Regression tests
protect the earlier Boolean/non-finite validation and safe error reporting.
These characterize existing behavior; no application behavior was changed.
Tests passing after implementation is characterization, not a claim that this
work was developed using TDD. Practice red-green-refactor in a separate scratch
exercise before applying it to the next feature. Coverage measures execution,
not whether assertions or requirements are correct.

In VS Code open this toolkit folder, select the new environment with
**Python: Select Interpreter**, then **Python: Configure Tests > pytest > tests**.
Use the terminal's default `python -m pytest -q` command for all configured
directories, including Day 7. Review changes manually before staging or pushing.


## Day 9 Data Validation Transformation and Algorithmic Thinking

The separate `data_toolkit.day09` package teaches a strict `transaction_id`,
`category`, `amount` contract without changing earlier `id` pipelines.
Read [Day 9 practical and policies](DAY9_PRACTICAL.md) for rules, expected output,
complexity, errors, test coverage and Windows setup.

```powershell
python day9_practicals.py
python -m pytest tests/day09 -v
python -m pytest -q
```

Validation reports rejected rows; transformation creates canonical copies;
statistics summarize accepted records. Numeric strings, Boolean amounts,
nonpositive/nonfinite amounts and later duplicate IDs are rejected.
No new dependencies are required beyond the existing pytest development entry.


## Day 10: CLI Design and Application Architecture

From this toolkit folder in PowerShell, use a working Python 3.12+ interpreter:

```powershell
$env:PYTHONPATH = (Join-Path (Get-Location) 'src')
python -m data_toolkit.cli --help
python -m data_toolkit.cli convert --help
python -m data_toolkit.cli validate samples/transactions.csv
python -m data_toolkit.cli analyze samples/transactions.csv
python -m data_toolkit.cli convert samples/transactions.csv --output output/transactions.json
python -m data_toolkit.cli report samples/transactions.json --output output/report.txt
$LASTEXITCODE
```

Use a new destination or intentionally add `--force` if output already exists.
Expected sample summary: 3 transactions, total 225.0, average 75.0,
minimum 50.0, maximum 100.0; food 2/175.0 and transport 1/50.0.
See [DAY10_PRACTICAL.md](DAY10_PRACTICAL.md) for contracts, failure drills,
architecture, output safety, test commands and interpreter troubleshooting.

New subcommands use the strict Day 9 contract: positive finite numeric amounts,
nonblank IDs/categories and no duplicate trimmed IDs. All rows must pass;
no invalid rows are silently discarded. CSV amount strings are parsed at the
file boundary; JSON numeric strings and Booleans are rejected. The adapter
accepts historical `id` or canonical `transaction_id`; conflicting fields fail.
Convert emits only `transaction_id`, `category`, `amount` in canonical JSON.
Report accepts JSON or CSV and emits UTF-8 text, reusing earlier report helpers.

`validate` and `analyze` print JSON to stdout. File-producing commands print a
JSON acknowledgement only after successful publication. Expected errors go to
stderr without tracebacks or raw transaction values. Paths may appear in file
errors. Exit statuses: 0 success/help, 1 data/file/output failure, 2 usage error.
Legacy direct-file/no-argument commands retain their original output, validation,
logging and historical error status 2. Top-level help now lists the subcommands.

```powershell
python -m data_toolkit.cli validate samples/day10_invalid.csv
# Exit 1: rows 2 and 3 are invalid.
python -m data_toolkit.cli convert samples/transactions.csv
# Exit 2: --output is required.
python -m pytest tests/day10 -q
python -m pytest -q
python run_day5_tests.py
```

No environment is recreated by this feature. If `python` is unavailable or a
venv points to a missing executable, invoke a verified Python with `& $py` and
install development requirements only in an environment you intend to manage.


## Day 11 optional document summaries with GroqCloud

The default provider is a deterministic offline mock. Setting a key never selects
live mode automatically. Choose `--provider groq` explicitly to send document text
to GroqCloud; no OpenAI API account or key is needed. The previous OpenAI adapter
and its adapter tests remain as historical code to preserve the existing staged
implementation. It is not a CLI choice and Groq does not import it.

### Windows PowerShell and VS Code setup

Open this repository in VS Code and select Terminal > New Terminal > PowerShell.
Use a working Python 3.10+ interpreter. If the old root `.venv` points to a missing
Python installation, create a separate ignored environment without deleting it:

```powershell
Set-Location 'C:\Users\USER\python-foundations\day03.py\python-data-toolkit'
py -m venv .venv-day11
& .\.venv-day11\Scripts\python.exe -m pip install -r requirements-dev.txt
$toolkitPython = Join-Path $PWD '.venv-day11\Scripts\python.exe'
$env:PYTHONPATH = (Join-Path $PWD 'src')
```

If `py` is unavailable, install a working Python with its Windows launcher or use
the full path to an existing interpreter instead of `py`. Select the same
interpreter in VS Code with Python: Select Interpreter. The Groq adapter uses the
standard library, so there is no Groq SDK or new runtime package to install.

Run the mock without a key, connection or API cost:

```powershell
& $toolkitPython -m data_toolkit.cli summarize samples/day11_operations.txt
& $toolkitPython -m data_toolkit.cli summarize --help
```

Expected: exit 0 and a four-field JSON object with title
`Quarterly Operations Report`, deterministic extractive summary/key points and
`open_questions: []`. Input is nonblank UTF-8 text, at most 20000 characters;
Word/PDF extraction is not included.

### Configure Groq privately and deliberately opt into a live request

Create a key in your [GroqCloud account](https://console.groq.com/keys).
The key is read exclusively from `GROQ_API_KEY`; `.env` files are not loaded
automatically. Enter it privately rather than putting a literal in command history:

```powershell
$groqKeyInput = Read-Host 'Groq API key (hidden)' -AsSecureString
$env:GROQ_API_KEY = [System.Net.NetworkCredential]::new('', $groqKeyInput).Password
Remove-Variable groqKeyInput
```

Never print, log, paste into chat or commit the key. Keep real keys out of source,
frontend code, tests, docs and screenshots. Environment values are plaintext while
in use; protect the terminal and machine. Existing `.env` and private-document
ignore rules are unchanged. Ignoring a file does not remove an already tracked
secret; revoke/rotate an exposed key at Groq.

The default model is `openai/gpt-oss-20b`, listed as a Groq production model with
strict structured-output support in the official documentation checked on
31 October 2026. Here `openai/` identifies the model publisher: the endpoint is
`https://api.groq.com/openai/v1/chat/completions` and requests go only to Groq.
The model is a general text model suited to this small document-summary task.
Optional `GROQ_MODEL` overrides the default; any replacement must support Groq Chat
Completions with strict JSON Schema (for example `openai/gpt-oss-120b`). Verify
current support and your account's model permissions before changing it.

The following command sends text externally and may incur API charges. Run it only
when you choose to make a live request; the implementation/tests do not need it:

```powershell
& $toolkitPython -m data_toolkit.cli summarize samples/day11_operations.txt --provider groq --timeout 15
```

The adapter makes one request, caps completion output at 2048 tokens, does not
stream, disables redirects and never retries or switches models automatically.
Check [current pricing/model availability](https://console.groq.com/docs/models),
account limits, quota and [spend controls](https://console.groq.com/docs/spend-limits).
Spend-limit availability depends on account tier and permissions; Groq documents
a delay in spend tracking, so limits should not be treated as precise per-call caps.
Do not assume free usage or unlimited credits. Input characters are not an exact
token budget. Start with a small public sample and inspect usage afterward.
A timed-out request may already have been processed; fallback cannot undo a charge.
Submit only documents you are authorized to disclose under applicable provider policies.

Clear the current session after use:

```powershell
Remove-Item Env:GROQ_API_KEY -ErrorAction SilentlyContinue
Remove-Item Env:GROQ_MODEL -ErrorAction SilentlyContinue
```

### Validation, errors and explicit fallback

The provider-independent `SummaryProvider` contract remains
`summarize(document, timeout=...) -> JSON text`. The service parses the result and
validates exactly `title`, `summary`, `key_points` and `open_questions`. Title and
summary must be nonblank strings of at most 200 and 2000 characters respectively.
Key points require 1–10 nonblank strings; open questions allow 0–10; every item is
at most 500 characters. Valid JSON alone does not establish valid application data
or factual accuracy. Strict provider output does not replace these checks or source review.

`--timeout` defaults to 15 seconds and must be finite, greater than 0 and at most
120. This bounds blocking socket operations, not a strict total elapsed deadline.
Responses over 128000 bytes, malformed envelopes, refusals, truncated completions,
invalid JSON and schema violations fail safely. Errors never display provider
response bodies, credentials, headers or document text.

| Failure | Action |
|---|---|
| Missing/invalid configuration | Set `GROQ_API_KEY` privately; check optional `GROQ_MODEL`. |
| Authentication 401 | Check or rotate the key locally; do not blindly retry. |
| Permission 403 / missing model 404 | Check project access and current model support. |
| Rate limit 429 | Wait, reduce throughput and check quota/usage. |
| Timeout / connection failure | Check connectivity; retry only by deliberate choice. |
| 5xx / capacity failure | Service unavailable; try later or select offline fallback. |
| Invalid/incomplete/refused AI response | Reject it; inspect offline tests or use fallback. |

Default failure is exit 1 and safe stderr; invalid CLI usage is exit 2. To explicitly
allow the mock on provider/response failure, add `--fallback`:

```powershell
& $toolkitPython -m data_toolkit.cli summarize samples/day11_operations.txt --provider groq --timeout 15 --fallback
```

On fallback, stdout still contains the four-field JSON and stderr clearly warns
that offline mock output was used. Library callers get `used_fallback=True`.
Input errors and invalid timeout settings still fail before a provider request.
The mock remains deterministic; a real model is not guaranteed deterministic.

### Tests with no internet, key or credits

```powershell
& $toolkitPython -m pytest -q tests/day11
& $toolkitPython -m pytest -q
```

All Day 11 tests clear real provider configuration and block socket connections.
Groq tests replace the HTTP boundary with local fake responses and nonfunctional
test placeholders. They verify authentication/rate/service/timeout errors, bounded
response handling, malformed/refused/truncated output, existing schema validation,
CLI selection and explicit fallback without using credits. Earlier regression tests
remain in the full suite. Live model/account compatibility is unverified until an
explicitly approved live request is made.

Official references: [Chat Completions API](https://console.groq.com/docs/api-reference),
[structured outputs](https://console.groq.com/docs/structured-outputs), and
[error codes](https://console.groq.com/docs/errors).

Migration changes are deliberately **unstaged**. Previously staged Day 11 content
remains in the index unchanged; a commit of the existing index alone would still
contain the older provider selection. Review working-tree changes before deciding
what to stage later. Private practical documents and `.gitignore` are preserved.
