"""Command-line wrapper around :func:`roman.to_roman`.

Usage:
    python cli.py 1954   ->  MCMLIV
"""

import sys

from roman import to_roman


def main(argv: list[str]) -> int:
    """Convert a single integer argument to a Roman numeral.

    Returns a process exit code: 0 on success, 2 on a usage or value error
    (matching the convention argparse uses for bad arguments).
    """
    if len(argv) != 1:
        print("usage: python cli.py <integer 1..3999>", file=sys.stderr)
        return 2
    try:
        print(to_roman(int(argv[0])))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
