#!/usr/bin/env python3
"""Everyday Things, Two Lines — entry program.

Writes a two-line explanation of a queue to /output/entry.txt:
line 1 explains the queue to a 10-year-old through one analogy,
line 2 says what that analogy maps and what it leaves out.
Standard library only, deterministic, no network.
"""

import os
import sys


class GateError(Exception):
    """Raised when the entry text fails the competition gate."""


class TwoLineEntry:
    """Holds the two entry lines and checks them against the gate."""

    MAX_CHARS = 400

    def __init__(self, first, second):
        self.lines = (first, second)

    def render(self):
        """Join the two lines into the exact file text."""
        return "\n".join(self.lines) + "\n"

    def validate(self, text):
        """Gate: UTF-8, 1-400 chars, not only whitespace, exactly 2 lines,
        each line exactly one sentence."""
        text.encode("utf-8")  # raises UnicodeEncodeError if not encodable
        if not (1 <= len(text) <= self.MAX_CHARS):
            raise GateError(f"length {len(text)} outside 1-{self.MAX_CHARS}")
        if not text.strip():
            raise GateError("text is only whitespace")
        lines = text.rstrip("\n").split("\n")
        if len(lines) != 2:
            raise GateError(f"expected 2 lines, found {len(lines)}")
        for line in lines:
            if not line.strip():
                raise GateError("an entry line is empty")
            if line != line.strip():
                raise GateError("an entry line has leading/trailing space")
            # One sentence: exactly one terminal mark, at the very end.
            closers = sum(line.count(mark) for mark in (".", "!", "?"))
            if closers != 1 or not line.rstrip().endswith("."):
                raise GateError(f"line is not a single sentence: {line!r}")
        return True

    def write_to(self, path):
        text = self.render()
        self.validate(text)
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        return text


ENTRY = TwoLineEntry(
    "A queue is a human train: everyone hooks up behind the person in front, "
    "and the whole line shuffles forward one carriage at a time whenever the "
    "door at the front opens.",
    "The train maps the order and the waiting, but it leaves out that "
    "carriages cannot choose to leave or swap places, while the people in a "
    "queue can.",
)


def main(argv):
    target = argv[1] if len(argv) > 1 else "/output/entry.txt"
    try:
        text = ENTRY.write_to(target)
    except GateError as exc:
        print(f"gate failed: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} chars, 2 lines -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
