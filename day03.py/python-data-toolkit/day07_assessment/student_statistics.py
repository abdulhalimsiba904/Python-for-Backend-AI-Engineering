"""Day 7, Problem 1: summarize student examination scores."""


def calculate_statistics(scores):
    """Return statistics for a list of valid numeric scores without changing it."""
    count = len(scores)
    if count == 0:
        return {
            "total": 0,
            "average": None,
            "highest": None,
            "lowest": None,
            "count": 0,
            "passed": 0,
            "failed": 0,
        }

    total = sum(scores)
    passed = 0
    for score in scores:
        if score >= 50:
            passed += 1

    return {
        "total": total,
        "average": round(total / count, 2),
        "highest": max(scores),
        "lowest": min(scores),
        "count": count,
        "passed": passed,
        "failed": count - passed,
    }
