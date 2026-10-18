#!/usr/bin/env python3
"""Check UTF-8 PR bodies for escaped prose newlines and control characters."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def check(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        return [f"{path}: invalid UTF-8: {error}"]

    errors: list[str] = []
    in_fence = False
    for line_number, line in enumerate(text.splitlines(), 1):
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
            continue
        if not in_fence and re.search(r"\\[nr]", line):
            errors.append(f"{path}:{line_number}: escaped newline/control sequence in prose")
        for character in line:
            codepoint = ord(character)
            if codepoint < 32 and character not in "\t\r\n":
                errors.append(f"{path}:{line_number}: disallowed control character U+{codepoint:04X}")
            if codepoint == 127:
                errors.append(f"{path}:{line_number}: disallowed control character U+007F")
    if in_fence:
        errors.append(f"{path}: unterminated fenced code block")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    errors = [error for path in args.paths for error in check(path)]
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Pull-request text checks passed: {len(args.paths)} UTF-8 file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
