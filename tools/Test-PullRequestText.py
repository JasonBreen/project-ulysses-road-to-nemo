#!/usr/bin/env python3
"""Check UTF-8 PR bodies for escaped prose newlines and control characters."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


WINDOWS_PATH = re.compile(r"(?<![A-Za-z0-9`])(?:[A-Za-z]:\\|\\\\)[^\s`]+")


def check_text(text: str, label: str) -> list[str]:
    errors: list[str] = []
    line_number = 1
    for character in text:
        codepoint = ord(character)
        if codepoint < 32 and character not in "\t\r\n":
            errors.append(f"{label}:{line_number}: disallowed control character U+{codepoint:04X}")
        if codepoint == 127:
            errors.append(f"{label}:{line_number}: disallowed control character U+007F")
        if character == "\n":
            line_number += 1

    in_fence = False
    for line_number, line in enumerate(text.split("\n"), 1):
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        path_spans = [match.span() for match in WINDOWS_PATH.finditer(line)]
        for match in re.finditer(r"\\[nr]", line):
            in_inline_code = line[: match.start()].count("`") % 2 == 1
            in_windows_path = any(start <= match.start() < end for start, end in path_spans)
            if not in_inline_code and not in_windows_path:
                errors.append(f"{label}:{line_number}: escaped newline/control sequence in prose")
    if in_fence:
        errors.append(f"{label}: unterminated fenced code block")
    return errors


def check(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        return [f"{path}: invalid UTF-8: {error}"]
    return check_text(text, str(path))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def self_test() -> None:
    positive = (
        r"A Windows path such as C:\repo\project is ordinary prose." + "\n"
        "An inline code example is `\\n`.\n"
        "```text\n"
        r"A fenced example may contain \n." + "\n```.\n"
    )
    require(not check_text(positive, "positive"), "positive path/code text was rejected")
    raw_control = "safe\vraw control"
    require(any("U+000B" in error for error in check_text(raw_control, "raw")), "vertical-tab mutation was accepted")
    escaped_prose = r"bad \n prose"
    require(check_text(escaped_prose, "escaped"), "escaped prose newline mutation was accepted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    errors = [error for path in args.paths for error in check(path)]
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Pull-request text checks passed: {len(args.paths)} UTF-8 file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
