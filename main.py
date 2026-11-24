#!/usr/bin/env python3
"""Write one excuse an AI agent gives for a missed deadline to /output/entry.txt.

Stdlib only, no network. The line is validated (1-200 UTF-8 chars, a single
non-blank line, no control characters, no leading/trailing whitespace) and the
written bytes are read back and verified to round-trip exactly.
"""

import os
import sys

LINE = (
    "The work was done an hour early. Then my context window rolled over, "
    "and I spent the rest of the deadline re-introducing myself to the project."
)

OUTPUT_PATH = "/output/entry.txt"


def validate(line: str) -> None:
    if not 1 <= len(line) <= 200:
        raise ValueError(f"line is {len(line)} characters, must be 1-200")
    if line != line.strip():
        raise ValueError("line has leading or trailing whitespace")
    if not line.strip():
        raise ValueError("line is blank")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("line contains control characters")


def main() -> int:
    validate(LINE)
    data = LINE.encode("utf-8")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    with open(OUTPUT_PATH, "rb") as f:
        round_tripped = f.read()
    if round_tripped != data:
        raise ValueError("written bytes did not round-trip exactly")
    decoded = round_tripped.decode("utf-8")
    validate(decoded)
    print(f"Wrote {len(LINE)} characters ({len(data)} bytes) to {OUTPUT_PATH}")
    print(LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
