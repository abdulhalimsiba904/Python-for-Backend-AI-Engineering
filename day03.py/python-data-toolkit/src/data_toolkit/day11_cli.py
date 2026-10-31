"""Day 11 UTF-8 summaries; GroqCloud is used only with explicit --provider groq."""
import argparse
import json
from pathlib import Path
import sys

from data_toolkit.summaries import SummaryError, summarize_document


def main(argv=None):
    parser = argparse.ArgumentParser(description='Summarize a UTF-8 text document.', allow_abbrev=False)
    parser.add_argument('file', type=Path)
    parser.add_argument('--provider', choices=['mock', 'groq'], default='mock')
    parser.add_argument('--timeout', type=float, default=15.0,
                        help='Socket timeout in seconds, greater than 0 and at most 120 (default: 15).')
    parser.add_argument('--fallback', action='store_true', help='Use labeled offline output on service failure.')
    args = parser.parse_args(argv)
    try:
        # Bounded read avoids loading an arbitrarily large input file.
        with args.file.open(encoding='utf-8-sig') as source:
            document = source.read(20001)
        provider = None
        if args.provider == 'groq':
            from data_toolkit.groq_summary import GroqSummaryProvider
            provider = GroqSummaryProvider()
        result = summarize_document(document, provider, timeout=args.timeout, fallback=args.fallback)
        print(json.dumps(result.summary.to_dict(), indent=2))
        if result.used_fallback:
            print('warning: Offline mock fallback used; this is not an AI summary.', file=sys.stderr)
    except (OSError, UnicodeError):
        print('error: Cannot read document; use an accessible UTF-8 text file.', file=sys.stderr)
        return 1
    except SummaryError as error:
        print(f'error: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
