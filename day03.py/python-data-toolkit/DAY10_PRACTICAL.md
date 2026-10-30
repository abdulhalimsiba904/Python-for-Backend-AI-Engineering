# Day 10 CLI practical

## Setup and commands

Open `C:\Users\USER\python-foundations\day03.py\python-data-toolkit` in VS Code.
Use Python: Select Interpreter to choose a working Python 3.12+ interpreter.
Open PowerShell in this folder; do not run the source module as a loose script.

```powershell
$env:PYTHONPATH = (Join-Path (Get-Location) 'src')
python -m data_toolkit.cli --help
python -m data_toolkit.cli validate samples/transactions.csv
python -m data_toolkit.cli analyze samples/transactions.csv
python -m data_toolkit.cli convert samples/transactions.csv --output output/transactions.json
python -m data_toolkit.cli report samples/transactions.json --output output/report.txt
python -m data_toolkit.cli report output/transactions.json --output output/from_converted.txt
$LASTEXITCODE
```

Check `$LASTEXITCODE` immediately after each external command. For a quoted
executable, use `$py = 'C:\path\to\python.exe'` then `& $py -m ...`.
The existing repo `.venv` may point to a missing WindowsApps Python; do not
delete or replace it as part of this lesson. Use a verified interpreter instead.
The terminal interpreter can differ from VS Code's selected interpreter.

## Architecture and contracts

- `cli.py` routes named commands to `day10_cli.main`; the original direct-file
  CLI remains available with its output, logs and validation rules unchanged.
- `day10_cli.py` declares argparse subcommands, prints results/errors, returns
  statuses, and calls application functions. Imports do not execute the CLI.
- `application.py` adapts existing readers to Day 9 validation/transformation,
  renders reports using Day 9 statistics plus existing reports helpers, and
  publishes output. It does not parse arguments or print diagnostics.
- Existing `day09` modules, readers and reports are reused without edits.

New commands accept `.csv`/`.json` case-insensitively. Existing samples use `id`;
Day 9 uses `transaction_id`. The adapter maps the historical spelling. Both
fields together must be equal. CSV amounts are text and are converted to float
before validation; JSON amounts must already be numeric. Booleans, JSON numeric
strings, nonpositive/nonfinite amounts and duplicate trimmed IDs fail. Extra
CSV fields fail; missing fields reach the Day 9 validator. Canonical conversion
outputs exactly transaction_id, category and amount; extra metadata is omitted.
IDs are trimmed and case-sensitive. Categories collapse whitespace and casefold.
All rows must pass: invalid rows are not silently removed. Data-row numbers are
one-based and exclude the CSV header. Empty JSON lists are accepted.

`validate` emits JSON validity/count. `analyze` emits the full unrounded Day 9
summary. `convert` writes canonical JSON and requires `.json` output. `report`
writes text and requires `.txt` output; it accepts CSV and JSON. Its average is
rounded by the earlier calculate_average helper; totals show two decimals.
This educational float model is not an accounting/currency contract.

The sample has count 3, total 225.0, mean 75.0, min 50.0, max 100.0; food
count 2/total 175.0 and transport count 1/total 50.0. Conversion JSON can be
fed directly to report. New commands print only JSON results/acknowledgements
to stdout. Expected errors go to stderr without tracebacks. Diagnostics avoid
raw record values, but OS file errors may include paths.

## Exit statuses and failures

0 means success/help; 1 means expected data/file/output failure; 2 means invalid
command syntax. The module guard raises SystemExit(main()) to set the process
status. argparse handles help and usage exits. Legacy direct-file usage retains
historical failure status 2. Top-level help now describes named commands;
no arguments still produces the earlier default sample report.

```powershell
python -m data_toolkit.cli validate samples/day10_invalid.csv
# 1: duplicate ID at row 2 and negative amount at row 3
python -m data_toolkit.cli validate samples/missing.json
# 1: file error
python -m data_toolkit.cli convert samples/transactions.csv
# 2: required --output missing
python -m data_toolkit.cli analyze --help
# 0: help
```

Quote paths with spaces. Relative paths are relative to the working directory,
not the source module. type=Path converts the argument but does not validate
existence. Set PYTHONPATH for application commands; pytest.ini sets it for tests.
Unknown command words fail through the legacy parser/load path with status 2.
Command words are reserved; prefix an identically named legacy file with `./`.

## Output safety

Validation and serialization finish before destination publication. Existing
destinations are refused unless `--force` is supplied. Input and output must
differ, including existing hard-link aliases. Existing destination symlinks
are refused. Missing parent directories are created. A securely created
same-directory temporary file is flushed and fsynced; publication is by hard
link without clobbering, or os.replace with --force. Temporary files are cleaned
in finally, including publication failure. A failed input does not overwrite
an earlier report even when --force is requested.

Use trusted local output directories. This requires filesystem support for hard
links/replacement; unsupported operations fail instead of falling back to direct
truncation. It is not a defense against hostile concurrent directory replacement
and is not a full power-loss durability guarantee. Forced replacement may change
file metadata because a newly created file replaces the previous one.

## Test and review

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest tests/day10 -q
python -m pytest -q
python run_day5_tests.py
```

Use a deliberately selected environment for installation. The implementation
session used bundled Python plus pytest installed in the chat workspace, without
altering `.venv`. Exact session results and invocation paths are in the delivered
completion report. Tests use subprocess with sys.executable, argument lists,
capture_output and timeouts; disposable tmp_path files protect real outputs.
Coverage includes help, syntax, exit status, strict validation, malformed data,
empty input, conversion/report integration, output protection, encoding errors
and simulated publication failure. Earlier CLI tests remain unchanged.

For independent practice, change an amount in a copy, predict its status, then
check both stdout and stderr. Explain why CSV text adaptation belongs at the
file boundary, and why business functions should neither parse args nor exit.

Review `git diff` and the explicit new files before staging. Do not use
`git add .`; keep private Day 6 notes and the unrelated untracked rc file out.
