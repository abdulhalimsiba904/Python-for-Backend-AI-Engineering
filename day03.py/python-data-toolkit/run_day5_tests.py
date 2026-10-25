"""Run every test function, with an optional filename for focused testing."""
from pathlib import Path
import runpy
import sys


def main() -> None:
    root = Path(__file__).resolve().parent
    # Find our src package even in a fresh terminal without PYTHONPATH.
    sys.path.insert(0, str(root / "src"))
    paths = [root / "tests" / sys.argv[1]] if len(sys.argv) > 1 else sorted((root / "tests").glob("test_*.py"))
    count = 0
    for path in paths:
        namespace = runpy.run_path(str(path))
        for name, function in namespace.items():
            if name.startswith("test_") and callable(function):
                function()
                count += 1
        print(f"PASS: {path.name}")
    if len(sys.argv) == 1:
        runpy.run_path(str(root / "test_toolkit.py"), run_name="__main__")
    print(f"Passed {count} test functions.")


if __name__ == "__main__":
    main()
