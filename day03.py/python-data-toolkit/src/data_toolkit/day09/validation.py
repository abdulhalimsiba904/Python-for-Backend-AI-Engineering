"""Validate raw records without normalization or input mutation."""
from copy import deepcopy
from math import isfinite


def validate_transactions(records: list) -> tuple[list[dict], list[dict]]:
    """Return independent valid copies and row/field errors in input order.

    IDs are compared after trimming, preserving case. Only the first valid
    occurrence reserves an ID. All detectable field errors are reported.
    Extra fields are allowed and deep-copied; inputs are ordinary data records.
    """
    if not isinstance(records, list):
        raise TypeError("transactions must be a list")
    valid, invalid = [], []
    seen = set()
    for number, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            invalid.append({"row": number, "errors": {
                "record": "must be a dictionary"}})
            continue
        errors = {}
        for field in ("transaction_id", "category", "amount"):
            if field not in record:
                errors[field] = "required field is missing"
        for field in ("transaction_id", "category"):
            if field in record:
                value = record[field]
                if not isinstance(value, str) or not value.strip():
                    errors[field] = "must be a nonblank string"
        if "amount" in record:
            amount = record["amount"]
            # bool inherits from int: check exact built-in numeric types.
            if type(amount) not in (int, float):
                errors["amount"] = "must be an int or float excluding bool"
            else:
                try:
                    numeric = float(amount)
                    if not isfinite(numeric) or numeric <= 0:
                        errors["amount"] = "must be positive and finite"
                except OverflowError:
                    errors["amount"] = "must be representable as a finite float"
        if "transaction_id" not in errors:
            key = record["transaction_id"].strip()
            if key in seen:
                errors["transaction_id"] = "duplicate ID"
        if errors:
            invalid.append({"row": number, "errors": errors})
        else:
            seen.add(key)
            valid.append(deepcopy(record))
    return valid, invalid
