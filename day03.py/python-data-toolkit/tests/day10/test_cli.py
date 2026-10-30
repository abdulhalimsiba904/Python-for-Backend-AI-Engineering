"""Day 10 tests exercise the real command boundary and disposable outputs."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]


def run(*args):
    return subprocess.run(
        [sys.executable, "-m", "data_toolkit.cli", *map(str, args)],
        cwd=ROOT, env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        capture_output=True, text=True, timeout=15,
    )


def input_file(tmp_path, records):
    path = tmp_path / "input file.json"
    path.write_text(json.dumps(records), encoding="utf-8")
    return path


@pytest.mark.parametrize("args", [("--help",), ("validate", "--help"),
    ("analyze", "--help"), ("convert", "--help"), ("report", "--help")])
def test_help(args):
    result = run(*args)
    assert result.returncode == 0
    assert "usage:" in result.stdout
    assert result.stderr == ""


@pytest.mark.parametrize("args", [("validate",), ("analyze",),
    ("convert", "samples/transactions.csv"), ("report", "samples/transactions.json"),
    ("validate", "samples/transactions.csv", "--unknown"), ("unknown-command",)])
def test_usage_errors(args):
    result = run(*args)
    assert result.returncode == 2
    assert result.stdout == ""
    assert "error:" in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("suffix", ["csv", "json"])
def test_validate_existing_samples(suffix):
    result = run("validate", f"samples/transactions.{suffix}")
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {"valid": True, "count": 3}
    assert result.stderr == ""


def test_analyze_existing_sample():
    result = run("analyze", "samples/transactions.csv")
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary == {"count": 3, "total": 225.0, "average": 75.0,
        "minimum": 50.0, "maximum": 100.0,
        "by_category": {"food": {"count": 2, "total": 175.0},
                        "transport": {"count": 1, "total": 50.0}}}


def test_convert_then_report(tmp_path):
    output = tmp_path / "new folder" / "converted.json"
    result = run("convert", "samples/transactions.csv", "--output", output)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["count"] == 3
    rows = json.loads(output.read_text(encoding="utf-8"))
    assert rows[0] == {"transaction_id": "TX1001", "category": "food", "amount": 100.0}
    report = tmp_path / "report.txt"
    result = run("report", output, "--output", report)
    assert result.returncode == 0, result.stderr
    text = report.read_text(encoding="utf-8")
    assert "Count: 3" in text and "Total: 225.00" in text
    assert "food: count=2, total=175.00" in text
    assert result.stderr == ""


@pytest.mark.parametrize("amount", [True, False, 0, -1, "25", None, float("inf")])
def test_strict_json_amounts(tmp_path, amount):
    path = input_file(tmp_path, [{"transaction_id": "PRIVATE-ID", "amount": amount, "category": "food"}])
    result = run("validate", path)
    assert result.returncode == 1
    assert result.stdout == ""
    assert "amount" in result.stderr
    assert "PRIVATE-ID" not in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("text", ["{", "{}", "[null]", '[{"id":"T1","transaction_id":"T2"}]'])
def test_bad_json_and_shape(tmp_path, text):
    path = tmp_path / "bad.json"
    path.write_text(text, encoding="utf-8")
    result = run("validate", path)
    assert result.returncode == 1
    assert result.stdout == "" and "error:" in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("name,content", [("empty.csv", ""),
    ("extra.csv", "id,amount,category\nT1,10,food,extra\n"),
    ("missing.csv", "id,amount\nT1,10\n"),
    ("bad.csv", "id,amount,category\nT1,not-number,food\n"),
    ("unsupported.txt", "hello")])
def test_bad_files(tmp_path, name, content):
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    result = run("validate", path)
    assert result.returncode == 1 and result.stdout == ""
    assert "Traceback" not in result.stderr


def test_duplicate_and_negative_sample():
    result = run("validate", "samples/day10_invalid.csv")
    assert result.returncode == 1
    assert "Row 2" in result.stderr and "duplicate ID" in result.stderr
    assert "Row 3" in result.stderr and "positive" in result.stderr


def test_missing_file(tmp_path):
    result = run("validate", tmp_path / "missing.json")
    assert result.returncode == 1 and "error:" in result.stderr


def test_empty_dataset(tmp_path):
    path = input_file(tmp_path, [])
    result = run("analyze", path)
    assert result.returncode == 0
    value = json.loads(result.stdout)
    assert value["count"] == 0 and value["average"] is None


def test_output_protection_and_force(tmp_path):
    output = tmp_path / "saved.json"
    output.write_text("ORIGINAL", encoding="utf-8")
    result = run("convert", "samples/transactions.csv", "--output", output)
    assert result.returncode == 1 and "--force" in result.stderr
    assert output.read_text() == "ORIGINAL"
    result = run("convert", "samples/day10_invalid.csv", "--output", output, "--force")
    assert result.returncode == 1 and output.read_text() == "ORIGINAL"
    result = run("convert", "samples/transactions.csv", "--output", output, "--force")
    assert result.returncode == 0
    assert len(json.loads(output.read_text())) == 3
    assert not list(tmp_path.glob(".data-toolkit-*.tmp"))


def test_input_cannot_be_output(tmp_path):
    path = input_file(tmp_path, [{"id": "T1", "amount": 10, "category": "food"}])
    original = path.read_bytes()
    result = run("convert", path, "--output", path, "--force")
    assert result.returncode == 1 and "differ" in result.stderr
    assert path.read_bytes() == original


def test_output_is_directory(tmp_path):
    output = tmp_path / "directory.json"
    output.mkdir()
    result = run("convert", "samples/transactions.csv", "--output", output, "--force")
    assert result.returncode == 1 and "Traceback" not in result.stderr
    assert not list(tmp_path.glob(".data-toolkit-*.tmp"))


def test_encoding_error(tmp_path):
    path = tmp_path / "bad.json"
    path.write_bytes(b"\xff\xfe")
    result = run("validate", path)
    assert result.returncode == 1 and "UTF-8" in result.stderr


def test_output_extension(tmp_path):
    result = run("convert", "samples/transactions.csv", "--output", tmp_path / "bad.txt")
    assert result.returncode == 1 and ".json" in result.stderr


def test_failed_publish_preserves_output_and_cleans_temp(tmp_path, monkeypatch):
    from data_toolkit.application import write_output
    source = tmp_path / "source.json"
    source.write_text("[]")
    destination = tmp_path / "target.json"
    destination.write_text("KEEP")
    def fail(*args):
        raise PermissionError("simulated locked destination")
    monkeypatch.setattr(os, "replace", fail)
    with pytest.raises(PermissionError):
        write_output(destination, "NEW", source, force=True)
    assert destination.read_text() == "KEEP"
    assert not list(tmp_path.glob(".data-toolkit-*.tmp"))


def test_report_normalizes_without_mutating_input():
    from copy import deepcopy
    from data_toolkit.application import render_report
    rows = [{"transaction_id": " T1 ", "amount": 10, "category": "  FOOD  "}]
    original = deepcopy(rows)
    assert "food: count=1, total=10.00" in render_report(rows)
    assert rows == original
