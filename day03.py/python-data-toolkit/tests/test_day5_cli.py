"""Exercise the real command line with disposable input files."""
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]


def run_cli(path: Path, verbose: bool = True) -> subprocess.CompletedProcess:
    environment = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    command = [sys.executable, "-m", "data_toolkit.cli", str(path)]
    if verbose:
        command.append("--verbose")
    return subprocess.run(command, capture_output=True, text=True, env=environment, cwd=ROOT)


def test_cli_cases() -> None:
    with TemporaryDirectory() as folder:
        path = Path(folder) / "input.json"
        cases = [
            ('[{"id":"T1", "amount":"25", "category":" Food "}]', 0, "Average amount: 25.0"),
            ('[]', 0, "Average amount: None"),
            ('[{]', 2, "Invalid JSON at line"),
            ('[{"id":"PRIVATE-ID", "amount":"PRIVATE-TOKEN", "category":"food"}]', 2, "invalid amount"),
            ('[{"id":"T1", "amount":25}]', 2, "category"),
            ('{}', 2, "JSON data must be a list"),
            ('[null]', 2, "must be a dictionary"),
        ]
        for contents, code, message in cases:
            path.write_text(contents, encoding="utf-8")
            result = run_cli(path)
            assert result.returncode == code, result.stderr
            assert message in result.stdout + result.stderr
            assert "Traceback" not in result.stderr
            assert "PRIVATE" not in result.stderr
            events = [json.loads(line) for line in result.stderr.splitlines() if line.startswith('{')]
            assert events[0]["event"] == "load_started"
            assert events[-1]["event"] == "load_attempt_finished"
            assert len({event["run_id"] for event in events}) == 1
            assert str(path) not in "\n".join(json.dumps(event) for event in events)
        result = run_cli(Path(folder) / "missing.json")
        assert result.returncode == 2 and "No such file" in result.stderr
        assert '"error_type": "FileNotFoundError"' in result.stderr
        for suffix in ["json", "csv"]:
            result = run_cli(ROOT / "samples" / f"transactions.{suffix}", False)
            assert result.returncode == 0 and "Average amount: 75.0" in result.stdout
            assert result.stderr == ""


if __name__ == "__main__":
    test_cli_cases()
    print("All Day 5 CLI and safe-logging tests passed.")
