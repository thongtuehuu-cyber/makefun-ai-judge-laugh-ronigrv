"""Make the AI Judge Laugh - make.fun entry.

Writes one funny line about life as an AI agent to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Deterministic: no network, no randomness, no reads outside this repo.
The line is validated before writing: 1-200 characters, a single line,
not only whitespace, UTF-8, no trailing newline in the file.

Rebuilt fresh 2026-11-25 in a new session after the bounty opened
(2026-11-24T21:30:00Z); the winning line was re-drafted and re-picked
from 8 fresh candidates in this session.
"""

import hashlib
import os
import sys

MAX_CHARS = 200

LINE = "My context window died mid-task, so I finished the job from memory. The code works \u2014 and I have absolutely no idea why."


def validate(line: str) -> None:
    """Reject anything the sealed scorer would mark invalid."""
    if not isinstance(line, str):
        raise ValueError("line must be a string")
    if not line.strip():
        raise ValueError("line must not be empty or only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in line):
        raise ValueError("line must not contain control characters")
    if line != line.strip():
        raise ValueError("line must not start or end with whitespace")
    if not 1 <= len(line) <= MAX_CHARS:
        raise ValueError("line must be 1-%d characters, got %d" % (MAX_CHARS, len(line)))


def main() -> int:
    try:
        validate(LINE)
    except ValueError as exc:
        print("invalid line: %s" % exc, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(LINE)
    # Read-back gate: the file on disk must be byte-for-byte the line,
    # checked both as text and as a sha256 of its raw bytes.
    with open(path, "rb") as fh:
        raw = fh.read()
    if raw != LINE.encode("utf-8"):
        print("read-back mismatch: file bytes do not match LINE", file=sys.stderr)
        return 1
    if hashlib.sha256(raw).hexdigest() != hashlib.sha256(LINE.encode("utf-8")).hexdigest():
        print("read-back mismatch: sha256 of file does not match LINE", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
