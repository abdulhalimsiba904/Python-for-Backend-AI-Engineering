
import csv
import json
from pathlib import Path


def read_json(file_path: str | Path) -> list[dict]:
    """Read a JSON file and return its contents as a list of dictionaries."""
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("JSON data must be a list.")

    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Every item in the JSON list must be a dictionary.")

    return data


def read_csv(file_path: str | Path) -> list[dict[str, str]]:
    """Read a CSV file and return its rows as a list of dictionaries."""
    path = Path(file_path)

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("CSV file is missing its header row.")

        return list(reader)
