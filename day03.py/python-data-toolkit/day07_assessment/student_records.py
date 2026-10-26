"""Read student records from a JSON list."""

import json


def load_student_records(file_path):
    """Return a JSON list; raise ValueError for missing or invalid JSON files.

    List items are returned unchanged. Other file access errors propagate.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as error:
        raise ValueError(f"Student records file not found: {file_path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in student records file: {file_path}") from error

    if not isinstance(data, list):
        raise ValueError(f"Expected a top-level JSON list in: {file_path}")

    return data
