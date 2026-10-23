import csv
import json
from pathlib import Path

from data_toolkit.readers import read_json


def read_csv(file_path: str | Path) -> list[dict[str, str]]:
    """Read a CSV file and return its rows as a list of dictionaries."""
    path = Path(file_path)

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("CSV file is missing its header row.")

        return list(reader)


def test_read_json():
    file_path = Path("samples/transactions.json")

    transactions = read_json(file_path)

    assert len(transactions) == 3
    assert transactions[0]["id"] == "TX1001"
    assert transactions[0]["amount"] == 100.0
    assert transactions[0]["category"] == "food"


def test_read_json_with_path_object():
    file_path = Path("samples/transactions.json")

    transactions = read_json(file_path)

    assert isinstance(transactions, list)
    assert all(isinstance(item, dict) for item in transactions)


def test_read_json_rejects_wrong_structure():
    file_path = Path("samples/invalid_structure.json")
    file_path.write_text(
        json.dumps({"id": "TX1001"}),
        encoding="utf-8",
    )

    try:
        read_json(file_path)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for a dictionary instead of a list.")
    finally:
        file_path.unlink(missing_ok=True)



def test_read_csv():
    from data_toolkit.readers import read_csv

    file_path = Path("samples/transactions.csv")
    transactions = read_csv(file_path)

    assert len(transactions) == 3
    assert transactions[0]["id"] == "TX1001"
    assert transactions[0]["amount"] == "100.0"
    assert transactions[0]["category"] == "food"


def test_read_csv_with_empty_file():
    file_path = Path("samples/empty.csv")
    file_path.write_text("", encoding="utf-8")

    try:
        from data_toolkit.readers import read_csv

        try:
            read_csv(file_path)
        except ValueError:
            pass
        else:
            raise AssertionError("Expected ValueError for an empty CSV file.")
    finally:
        file_path.unlink(missing_ok=True)

    

if __name__ == "__main__":
    test_read_json()
    test_read_json_with_path_object()
    test_read_json_rejects_wrong_structure()
    test_read_csv()
    test_read_csv_with_empty_file()

    print("All reader tests passed.")


    