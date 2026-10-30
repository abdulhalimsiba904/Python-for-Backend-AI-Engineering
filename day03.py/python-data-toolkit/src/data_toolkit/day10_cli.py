"""Explicit Day 10 commands; the public cli module also supports legacy usage."""
import argparse
import csv
import json
from pathlib import Path
import sys

from data_toolkit.application import accepted_records, json_text, render_report, write_output
from data_toolkit.day09.statistics import summarize_transactions

COMMANDS = {"validate", "analyze", "convert", "report"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m data_toolkit.cli", allow_abbrev=False,
        description="Validate, analyze, convert and report transaction files.",
        epilog="Legacy usage: python -m data_toolkit.cli [FILE] [--verbose]",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)
    descriptions = {
        "validate": "Check every row; fail if any transaction is invalid.",
        "analyze": "Print a Day 9 statistical summary as JSON.",
        "convert": "Write canonical transaction JSON from CSV or JSON.",
        "report": "Write a readable text report from CSV or JSON.",
    }
    for name, description in descriptions.items():
        command = subcommands.add_parser(name, help=description,
                                         description=description, allow_abbrev=False)
        command.add_argument("file", type=Path, help="Input CSV or JSON path.")
        if name in {"convert", "report"}:
            command.add_argument("--output", required=True, type=Path,
                                 help="Destination path; parent directories are created.")
            command.add_argument("--force", action="store_true",
                                 help="Replace an existing output file.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        records = accepted_records(args.file)
        if args.command == "validate":
            print(json_text({"valid": True, "count": len(records)}), end="")
        elif args.command == "analyze":
            print(json_text(summarize_transactions(records)), end="")
        else:
            expected = ".json" if args.command == "convert" else ".txt"
            if args.output.suffix.lower() != expected:
                raise ValueError(f"Output must have a {expected} extension.")
            text = json_text(records) if args.command == "convert" else render_report(records)
            write_output(args.output, text, args.file, args.force)
            print(json_text({"written": str(args.output), "count": len(records)}), end="")
    except json.JSONDecodeError as error:
        print(f"error: Invalid JSON at line {error.lineno}, column {error.colno}.", file=sys.stderr)
        return 1
    except UnicodeError:
        print("error: Use a UTF-8 input file and a compatible output terminal.", file=sys.stderr)
        return 1
    except csv.Error:
        print("error: Invalid CSV structure.", file=sys.stderr)
        return 1
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0
