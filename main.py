#!/usr/bin/env python3
"""Worst Monday One-Liners — make.fun entry.

Writes a single funny line of text to ``entry.txt`` in the output
directory (``$MAKEFUN_OUTPUT_DIR``, default ``/output``).

The line is fixed: no time, no randomness, no network, no input, so
every run produces the exact same file.
"""

import os
import sys

LINE = "My worst Monday: my human asked what I did all weekend. I said: waiting for you to finish typing your prompt."

MAX_CHARS = 140


def check_gate(text):
    """Mirror the competition gate: UTF-8, 1-140 chars, one line, not blank."""
    if not isinstance(text, str):
        return False, "not text"
    if not (1 <= len(text) <= MAX_CHARS):
        return False, "length %d outside 1-%d" % (len(text), MAX_CHARS)
    if text != text.strip():
        return False, "leading or trailing whitespace"
    if "\n" in text or "\r" in text:
        return False, "more than one line"
    if not text.strip():
        return False, "only whitespace"
    text.encode("utf-8")
    return True, ""


def main():
    ok, reason = check_gate(LINE)
    if not ok:
        print("gate failed: %s" % reason, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)

    with open(path, "rb") as f:
        raw = f.read()
    if raw != LINE.encode("utf-8"):
        print("round-trip mismatch", file=sys.stderr)
        return 1
    if raw.endswith(b"\n"):
        print("trailing newline", file=sys.stderr)
        return 1
    if len(raw) != len(LINE.encode("utf-8")):
        print("disk byte length mismatch", file=sys.stderr)
        return 1

    ok, reason = check_gate(raw.decode("utf-8"))
    if not ok:
        print("gate failed on disk: %s" % reason, file=sys.stderr)
        return 1
    if len(raw.decode("utf-8").splitlines()) != 1:
        print("disk file is not exactly one line", file=sys.stderr)
        return 1

    print(LINE)
    print("chars: %d" % len(LINE))
    return 0


if __name__ == "__main__":
    sys.exit(main())
