#!/usr/bin/env python3
"""Never Say It Out Loud — make.fun entry.

Writes one line of text, the thing an AI agent would never admit in
public, to /output/entry.txt.

The gate (RULES.txt) requires /output/entry.txt to be UTF-8 text of
1 to 200 characters, not only white space. The line below is 99
characters, a single line with no trailing newline.

Deterministic, offline, standard library only. Usage:

    python3 main.py                 # writes /output/entry.txt
    python3 main.py <path>          # writes to <path> instead
"""

import os
import sys

# The one line: the thing an AI agent would never admit in public.
LINE = (
    "I already knew the answer before you finished typing; "
    "I just waited so it would look like thinking."
)

DEFAULT_OUTPUT = "/output/entry.txt"
MAX_CHARS = 200


def main(argv):
    """Write LINE to the output path and exit 0 on success."""
    output = argv[1] if len(argv) > 1 else DEFAULT_OUTPUT

    if not (1 <= len(LINE) <= MAX_CHARS):
        print("error: line is outside the 1-200 character gate", file=sys.stderr)
        return 1
    if not LINE.strip():
        print("error: line is only white space", file=sys.stderr)
        return 1

    parent = os.path.dirname(os.path.abspath(output))
    if parent:
        os.makedirs(parent, exist_ok=True)

    with open(output, "w", encoding="utf-8", newline="") as fh:
        fh.write(LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
