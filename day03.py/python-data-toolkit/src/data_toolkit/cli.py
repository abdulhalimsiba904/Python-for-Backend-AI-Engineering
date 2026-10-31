
import argparse
import json
import logging
from uuid import uuid4

from data_toolkit.processing import load_transactions
from data_toolkit.reports import calculate_average, count_categories
from data_toolkit.validators import find_duplicate_ids

logger = logging.getLogger(__name__)


def _legacy_main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Read transaction data and generate a summary."
    )
    parser.add_argument(
        "file",
        nargs="?",
        default="samples/transactions.json",
        help="Path to a JSON or CSV transaction file.",
    )
    parser.add_argument("--verbose", action="store_true", help="Show safe progress logs.")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING,
                        format="%(message)s")
    run_id = uuid4().hex

    def log_event(level: int, event: str, **details) -> None:
        # Only pass allowlisted metadata: never records, IDs, values or paths.
        logger.log(level, json.dumps({"event": event, "run_id": run_id,
                                    "entry_point": "cli", **details}))

    log_event(logging.INFO, "load_started")
    try:
        transactions = load_transactions(args.file)
    except json.JSONDecodeError as error:
        log_event(logging.WARNING, "load_failed", error_type="JSONDecodeError")
        parser.error(f"Invalid JSON at line {error.lineno}, column {error.colno}. Check commas and quotes.")
    except (OSError, ValueError) as error:
        log_event(logging.WARNING, "load_failed", error_type=type(error).__name__)
        parser.error(str(error))
    else:
        log_event(logging.INFO, "load_succeeded", record_count=len(transactions))
    finally:
        log_event(logging.INFO, "load_attempt_finished")

    amounts = [transaction["amount"] for transaction in transactions]
    average = calculate_average(amounts)
    category_counts = count_categories(transactions)
    duplicate_ids = find_duplicate_ids(transactions)

    print("=== Python Data Toolkit ===")
    print(f"Input file: {args.file}")
    print(f"Transaction count: {len(transactions)}")
    print(f"Average amount: {average}")
    print(f"Category counts: {category_counts}")
    print(f"Duplicate IDs: {duplicate_ids}")


def main(argv=None):
    """Route explicit Day 10 commands while preserving earlier invocation forms."""
    import sys
    from data_toolkit.day10_cli import COMMANDS, main as command_main
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments and arguments[0] == "summarize":
        from data_toolkit.day11_cli import main as summary_main
        return summary_main(arguments[1:])
    if arguments and (arguments[0] in COMMANDS
                      or arguments[0] in {"-h", "--help"}):
        return command_main(arguments)
    _legacy_main(arguments)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

