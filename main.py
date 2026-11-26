"""Fortune Cookie Funnies for Engineers — make.fun entry.

Writes one original fortune cookie message for a software engineer to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt when set).

The message is a fixed string: no network, no model calls, no randomness.
It is validated before writing: exactly one line, 1-120 characters,
no control characters.
"""

import os
import sys

ENTRY = "You will ask the AI to write the code. The AI will ask you to debug it."

MAX_CHARS = 120


def validate(text):
    """Return an error string, or None when the text passes the gate."""
    if not text or not text.strip():
        return "entry is empty or only whitespace"
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    if len(text) > MAX_CHARS:
        return "entry is %d characters, over the 120-character limit" % len(text)
    bad = [c for c in text if ord(c) < 0x20 or c == "\x7f"]
    if bad:
        return "entry contains control characters: %r" % bad
    # The brief requires a REAL fortune cookie message for an engineer:
    # a fortune (a prophecy about the reader) and an engineer cue.
    lowered = text.lower()
    if not any(op in lowered for op in ("you will", "you are", "your ", "soon", "beware")):
        return "entry must read as a fortune (a prophecy about the reader)"
    engineer_cues = ("code", "debug", "deploy", "merge", "bug", "ai", "engineer", "server", "test")
    if not any(cue in lowered for cue in engineer_cues):
        return "entry must carry an engineer cue"
    # The brief weighs freshness: a stock joke from a mug or a conference
    # slide loses to a line nobody has seen before. Reject the stock lines
    # the field is saturated with, so only a fresh line can pass.
    stock_jokes = (
        "it works on my machine", "have you tried turning it off",
        "friday deploy", "merge conflict", "404", "works on my machine",
        "there are only 10 kinds of people", "it is not a bug",
    )
    if any(stock in lowered for stock in stock_jokes):
        return "entry is a stock joke, not a fresh line"
    return None


def main():
    error = validate(ENTRY)
    if error is not None:
        print("invalid entry: %s" % error, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY + "\n")
    print("wrote %s (%d characters)" % (path, len(ENTRY)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
