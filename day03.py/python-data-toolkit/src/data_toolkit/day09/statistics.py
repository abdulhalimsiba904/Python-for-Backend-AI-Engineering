"""Deterministic summaries of accepted transactions using finite floats."""
from math import fsum

from .transformation import transform_transactions


def _total(amounts: list[float]) -> float:
    # Sorting fixes addition order across permutations of the same records.
    try:
        return fsum(sorted(amounts))
    except OverflowError:
        raise ValueError("transaction total exceeds finite float range") from None


def summarize_transactions(records: list) -> dict:
    """Return count/total/mean/extrema and sorted category counts/totals.

    Empty totals are 0.0; undefined empty mean/extrema are None.
    Invalid direct input raises; the caller must handle validation rejects.
    """
    clean = transform_transactions(records)
    amounts = [record["amount"] for record in clean]
    groups = {}
    for record in clean:
        groups.setdefault(record["category"], []).append(record["amount"])
    total = _total(amounts)
    return {
        "count": len(clean), "total": total,
        "average": total / len(clean) if clean else None,
        "minimum": min(amounts) if clean else None,
        "maximum": max(amounts) if clean else None,
        "by_category": {
            category: {"count": len(groups[category]),
                       "total": _total(groups[category])}
            for category in sorted(groups)
        },
    }
