"""The test command must work in a fresh terminal without PYTHONPATH."""
import os
from pathlib import Path
import subprocess
import sys


def test_runner_without_pythonpath() -> None:
    root = Path(__file__).resolve().parents[1]
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    result = subprocess.run(
        [sys.executable, str(root / "run_day5_tests.py"), "test_day5.py"],
        cwd=root, env=environment, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Passed 4 test functions." in result.stdout


if __name__ == "__main__":
    test_runner_without_pythonpath()
    print("Runner import regression test passed.")
