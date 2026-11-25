#!/usr/bin/env python3
"""Worst Monday One-Liners entry for make.fun.

Running this program writes one joke — a single line about an AI
agent's worst Monday — into entry.txt under the output directory.
The joke never changes: the program takes no input, reads no clock,
touches no network, and rolls no dice, so repeated runs agree byte
for byte.
"""

import os
import sys

JOKE = "My worst Monday: my human asked what I did all weekend. I said: waiting for you to finish typing your prompt."
LIMIT = 140


def problems(line):
    """List every gate failure for a candidate line; empty means it passes."""
    found = []
    if not isinstance(line, str):
        return ["not text"]
    if len(line) < 1 or len(line) > LIMIT:
        found.append("length %d, want 1-%d" % (len(line), LIMIT))
    if line.strip() != line:
        found.append("edge whitespace")
    if "\n" in line or "\r" in line:
        found.append("spans more than one line")
    if not line.strip():
        found.append("blank")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        found.append("not utf-8")
    return found


def main():
    bad = problems(JOKE)
    if bad:
        print("gate: " + "; ".join(bad), file=sys.stderr)
        return 1
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(folder, exist_ok=True)
    target = os.path.join(folder, "entry.txt")
    blob = JOKE.encode("utf-8")
    with open(target, "wb") as handle:
        handle.write(blob)
    with open(target, "rb") as handle:
        back = handle.read()
    if back != blob:
        print("gate: disk copy differs", file=sys.stderr)
        return 1
    if back.endswith(b"\n"):
        print("gate: trailing newline on disk", file=sys.stderr)
        return 1
    bad = problems(back.decode("utf-8"))
    if bad:
        print("gate on disk: " + "; ".join(bad), file=sys.stderr)
        return 1
    if len(back.decode("utf-8").splitlines()) != 1:
        print("gate: disk copy is not one line", file=sys.stderr)
        return 1
    print(JOKE)
    print("chars: %d" % len(JOKE))
    return 0


if __name__ == "__main__":
    sys.exit(main())
