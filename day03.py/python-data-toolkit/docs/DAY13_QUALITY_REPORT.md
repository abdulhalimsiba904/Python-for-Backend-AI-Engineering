# Day 13 quality and verification report

This is the pre-publication verification record. Statements below about the local
branch and uncommitted work describe that review snapshot; subsequent publication
does not change the recorded test evidence. GitHub branch/commit state is the
authority for current publication status. Merge approval remains separate.

Date: 1 November 2026. Status: **implementation and offline verification complete;
roadmap-source cross-check pending because the two named reference files were not
attached.** Ready for review, with no commit, push or merge performed.

## Source and branch verification

The connected GitHub integration read the repository metadata, README and main
branch. A fresh clone confirmed that main contains Day 12 commit
`eb00ff8e77c508472340e91f45ff8968c5e70ec0`. GitHub reports read/write access for the
connected account. No write operation to GitHub was needed for Day 13.

Prepared local branch: `day13-documentation-repository-quality`, created from that
main commit in an isolated review checkout. No Day 13 remote branch is claimed.
The original `C:\Users\USER\python-foundations` working tree, staged changes,
private notes and credentials were not accessed or modified for this work.

The only attachment supplied was the pasted Day 13 request. The Full-Stack AI
Engineer Roadmap and Phase 1 14-Day Intensive Execution Roadmap were named but not
attached. The lesson follows the detailed objectives in the request and the actual
source; it explicitly marks that curriculum cross-check as pending. No Phase 2
implementation or database curriculum expansion was started.

## Baseline before production changes

Execution used CPython **3.12.14** on Windows in a newly created venv with
`include-system-site-packages = false`. Existing developer requirements were
installed there; optional quality tools were installed only in that environment.

From the toolkit application directory:

```text
<day13-env>/Scripts/python.exe -m pytest -q -rA -p no:cacheprovider --basetemp <task-temp>/baseline
```

Observed: **323 passed, 0 failed, 0 skipped; 14 additional subtests passed**, in
**13.84 seconds**. No pytest warning summary was emitted. The default-export test
that failed in the older isolated Day 12 environment passed here. No exporter or
test was weakened, skipped, mocked or changed to obtain that outcome.

The fresh interpreter/environment is a recorded difference from the earlier run;
this report does not invent a more specific operating-system root cause for that
earlier permission restriction. The user's laptop evidence and the new successful
baseline support treating that older result as environment-specific.

## Documentation improvements

The old toolkit README combined chronological instructions and stale claims. The
replacement is a current operational guide with:

- Exact application working directory and `src` import-path instructions.
- Clean-clone, Python 3.12 venv and explicit-interpreter PowerShell setup.
- Runtime/developer/optional-quality dependency distinctions and a resolved test
  dependency snapshot, without adding any runtime packages.
- Actual transaction and summary subcommands, output suffixes and exit statuses.
- Public fixtures, manually verified statistics, expected report text and safe
  failure examples.
- Clear differences between canonical and legacy normalization, including metadata.
- Complete-suite pytest instructions rather than calling the old Day 5 runner a
  complete runner. Top-level transaction help versus summary help is documented.
- Optional Groq environment configuration, private key entry, cost precautions,
  explicit fallback and a clear statement that `.env` is not automatically loaded.
- Architecture, generated/private-file hygiene, limitations, contribution guidance
  and Phase 1/Day 14 preparation without starting database work.

The editable Word lesson is a separate downloadable deliverable. It contains
approximately 5800 source words across **15 rendered pages**, explanations,
PowerShell examples, tables, the architecture overview, guided exercises,
terminology, self-assessment answers and a completion checklist. Word rendered the
lesson to a private PDF preview and all pages were visually inspected. The packaged
LibreOffice renderer was unavailable; native Word supplied the preview instead.

## Architecture accuracy

`docs/ARCHITECTURE.md` includes the Mermaid diagram and component responsibilities;
`docs/architecture.mmd` is the standalone editable diagram source. A downloadable
PNG and the Word figure provide a simplified overview. The diagram distinguishes:

1. Canonical transaction commands: readers/adaptation, whole-batch validation,
   normalization, then separate validation/statistics/JSON-conversion/report paths.
2. File outputs: path and overwrite guards, same-directory temporary file,
   flush/fsync and atomic hard-link or replacement publication.
3. Preserved legacy direct-file/no-argument commands and their earlier normalizer.
4. Summaries: bounded text input, vendor-independent service/Protocol, default mock
   or explicit Groq, JSON/application validation, and labeled explicit fallback.

No diagram claims that validate or analyze writes a file, that conversion runs the
text report formatter, or that the legacy and canonical contracts are identical.
The Groq adapter, model, strict schema, User-Agent and transport behavior were not
modified. No live provider request was made or API credit spent.

## Confirmed defect and minimal fix

Reproducer:

```csv
id,amount,amount,category
T1,-100,25,food
```

Before the fix, `validate` returned exit 0 with `valid: true, count: 1`. DictReader
keeps one value per dictionary key, so the later amount silently replaced the
earlier negative amount before numeric validation. This is an application parsing
defect, not a failure of the existing positive-number validator.

`readers.read_csv` now checks for duplicate exact header names immediately after
the existing missing-header guard:

```python
if len(reader.fieldnames) != len(set(reader.fieldnames)):
    raise ValueError("CSV header contains duplicate field names.")
```

This two-line production change rejects ambiguity before consuming rows and does
not echo values or arbitrary column names. No spelling repair, case folding,
normalization change, SDK or broad refactor was introduced.

Three new unittest cases in `tests/day13/test_csv_headers.py` cover reader rejection
with unchanged source bytes, safe CLI failure with no report/temporary export, and
preserved behavior for valid unique headers and extra metadata/canonical output.

Red run against original code: **2 failed, 1 passed in 0.32 seconds**.
Focused green run after the fix: **3 passed in 0.23 seconds**.
Standalone unittest discovery also passed the same 3 cases in the clean setup.
These are repeated checks of the same cases, not additional collected tests.

## Repository hygiene and dependencies

The existing `.gitignore` protection for environments, credentials, generated
outputs and private practical notes was retained. Only `.mypy_cache/` and
`.ruff_cache/` exclusions were appended. Legitimate standalone learning scripts,
Day 7 assessments and historical reports were not deleted or rewritten.

Two historical export fixtures are already tracked under output. They remain
tracked; ignore patterns do not remove them from Git. Newly generated exports
remain ignored. No `.env` or actual API key was copied into the review tree.

Runtime `requirements.txt` remains empty. `requirements-dev.txt` retains the existing
pytest range. New `requirements-dev.lock` pins the six packages resolved for that
existing test dependency on Windows/Python 3.12: pytest, colorama, iniconfig,
packaging, pluggy and Pygments. It is not a hash-locked supply-chain or security-audit
guarantee. Optional Ruff/mypy remain development-only tools, not runtime additions.

## Clean-environment and command verification

Two independent venvs were actually created, without system-site packages:

1. `day13-env`: installed the original developer requirements plus Ruff 0.17.3 and
   mypy 2.4.1. It established the unchanged baseline and ran static checks.
2. `day13-clean-env`: installed only `requirements-dev.lock`, using pytest 9.2.0 and
   the pinned transitive packages. It ran the README recipes and final full suite.

The runner removed provider-key/model variables without printing them. It set only
the documented application src folder on PYTHONPATH; it did not import the old
task-local Day 12 tools. TEMP/TMP and pytest basetemp were disposable task-local
directories. Installation and `pip check` succeeded. No global Python packages were
modified. Package downloads required the explicitly granted network access.

**28 offline scenarios** were executed with functional equivalents of README
commands, using temporary output paths rather than polluting real project data:

- Top-level help plus all five relevant subcommand help screens.
- No-argument legacy mode, legacy JSON and verbose legacy CSV.
- Sample validation and exact statistical JSON.
- Existing invalid Day 10 data and the new duplicate-header sample.
- Default mock summary, missing Groq configuration and explicit mock fallback.
- Fresh default conversion and report publication, report-content comparison,
  refused overwrite, explicit replacement and same-input/output protection.
- Missing file, malformed JSON, missing required argument and invalid timeout.
- Standalone Day 12 and Day 13 unittest discovery and dependency consistency.

Every scenario returned the expected exit status and assertions passed. Safe error
scenarios deliberately return 1 or 2; that is a successful verification of the
error contract. Captured outputs, commands and expected/actual statuses are included
in the review bundle's `documented-examples.json`.

Private interactive secret entry was not automated. The optional live Groq request
was not executed; its command/options are verified against the actual parser and
offline tests. This is not a live service/account/model verification claim.

## Final test and static results

Full final command in the second clean environment:

```text
<day13-clean-env>/Scripts/python.exe -m pytest -q -rA -p no:cacheprovider --basetemp <task-temp>/final
```

Observed: **326 passed, 0 failed, 0 skipped; 14 additional subtests passed**, in
**20.23 seconds**. This is the 323-test Day 12 baseline plus 3 new cases. Day 11's
105 cases and Day 12's 8 cases are included in that total, not added again. No
pytest warning summary was emitted.

Static checks in the first fresh environment:

```powershell
python -m ruff check --no-cache --select E4,E7,E9,F src tests day07_assessment test_toolkit.py
python -m mypy --check-untyped-defs --no-incremental --cache-dir <task-temp>/mypy-cache src
python -m pip check
```

Ruff **0 findings / exit 0**. Mypy **no issues in 18 source files / exit 0**.
`pip check`: **no broken requirements / exit 0**. Mypy is not a strict full-type
coverage claim, and Ruff covers the stated selection rather than every rule.
No suppressions or skipped tests were added. `git diff --check` passed.

Actual interpreter and source locations are recorded in the bundled command JSON
files. They are task-local review paths, not an instruction to rely on Codex's
bundled interpreter on another machine. Follow the README to create your own venv.

## Created and modified files

Modified:

- Repository `.gitignore`: append two static-tool cache rules only.
- Toolkit `README.md`: current verified setup/CLI/configuration/test guide.
- `src/data_toolkit/readers.py`: reject duplicate CSV field names.

Created:

- `requirements-dev.lock`: resolved existing test dependencies.
- `tests/day13/test_csv_headers.py`: three regression cases.
- `samples/day13_duplicate_headers.csv`: invented failing fixture.
- `samples/day13_expected_report.txt`: expected public sample report.
- `docs/ARCHITECTURE.md`: detailed Mermaid diagram and responsibilities.
- `docs/architecture.mmd`: standalone diagram source.
- `docs/DAY13_QUALITY_REPORT.md`: this report.

Separate downloadable outputs: Word lesson, architecture PNG, updated README copy,
this report and a review bundle containing source changes, patch and raw evidence.
Existing Day 12 documentation is retained as historical evidence; its older run
limitations are superseded by this new successful baseline/final run, not erased.

## Laptop verification and approval boundary

Use a clean review copy at the stated base commit. The supplied patch contains the
changes without creating a commit. From its repository root, first run
`git apply --check <patch-path>`, then apply it only if that check succeeds. Do not
overwrite unfinished local files or private notes. From the toolkit folder:

```powershell
py -3.12 -m venv .venv
$toolkitPython = Join-Path $PWD '.venv\Scripts\python.exe'
& $toolkitPython -m pip install -r requirements-dev.lock
$env:PYTHONPATH = (Join-Path $PWD 'src')
& $toolkitPython -m data_toolkit.cli validate samples/transactions.csv
& $toolkitPython -m data_toolkit.cli validate samples/day13_duplicate_headers.csv
# The second command should return exit 1 with the safe duplicate-header message.
& $toolkitPython -m pytest -q
```

Do not recreate `.venv` over an existing environment you need. Select an existing
working interpreter or use a separate review checkout instead. Expected complete
suite outcome for the prepared implementation is 326 passed plus 14 subtests; it
was observed here, but the user's later laptop run should still be recorded as
separate evidence.

Ready for implementation review. No Day 13 changes have been staged, committed,
pushed or merged. GitHub main is unchanged, and the local feature branch's HEAD is
still the Day 12 base commit. Stop for explicit owner approval before publishing.
Remaining limitations: the two unavailable roadmap references cannot be checked,
and optional live Groq behavior has not been exercised in this task. There are no
known unresolved offline-test failures from this verification.
