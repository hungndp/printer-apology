#!/usr/bin/env python3
"""The Printer Apology — entrypoint.

Writes one one-line apology from an office printer to the people who
keep jamming it, feeding it cheap paper and swearing at it, to
/output/entry.txt (or $ENTRY_OUTPUT).

The line is built from two pieces so the joke's shape stays visible:
SETUP carries the apology and the incident, PUNCH carries the twist,
and the twist word ("napkin") lands last.
"""

import os
import sys

# --- The line, in two parts -------------------------------------------
# SETUP: the apology + the one incident (the jam).
SETUP = "Sorry I jammed your report. The paper was so thin"

# PUNCH: the reversal — the human's cheap paper is the real culprit,
# and the staple (a fellow sufferer) delivers the verdict.
# The twist word lands last; nothing follows the landing.
PUNCH = "the staple mistook it for a napkin."


def build_line() -> str:
    """Join setup and punch into the single entry line.

    The entry must be exactly one line: refuse any newline that
    ever creeps into either half instead of shipping it.
    """
    line = f"{SETUP} {PUNCH}"
    if "\n" in line or "\r" in line:
        raise ValueError("entry line must be a single line")
    return line


def output_path() -> str:
    """Where the entry goes: $ENTRY_OUTPUT, else /output/entry.txt."""
    return os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def main() -> int:
    """Write the line deterministically and print it."""
    line = build_line()
    if not (1 <= len(line) <= 120):
        print(f"line is {len(line)} chars, must be 1-120", file=sys.stderr)
        return 1
    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    # No trailing newline: the file is exactly the one line, byte for byte.
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
