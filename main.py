#!/usr/bin/env python3
"""Make the AI Judge Laugh: the Office Joke Open.

Writes a single one-line joke about office life to entry.txt in the
output directory (MAKEFUN_OUTPUT_DIR, or /output when that is unset).
Deterministic, stdlib only, no network, no reads outside this repo.
"""

import hashlib
import os
import sys

MAX_CHARS = 200

LINE = (
    "Our daily standup ran so long HR filed a missing-persons report "
    "for my motivation — last seen loitering by the coffee machine."
)


def validate(line: str) -> None:
    """Enforce the competition rules for the one-liner."""
    if not line:
        raise ValueError("line is empty")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line (no newline characters)")
    if "  " in line:
        raise ValueError("line must not contain double spaces")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("line must not contain control characters")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"line is {len(line)} characters, over the {MAX_CHARS} limit"
        )


def main() -> int:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    # Round-trip check: what landed on disk must be exactly the line,
    # byte for byte, with no trailing newline added by accident.
    with open(path, "rb") as fh:
        on_disk = fh.read()
    if on_disk != data:
        raise RuntimeError("written entry.txt does not match the line")
    if len(on_disk) != len(data):
        raise RuntimeError("written entry.txt has unexpected byte length")
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {len(data)} bytes to {path}")
    print(f"characters: {len(LINE)}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
