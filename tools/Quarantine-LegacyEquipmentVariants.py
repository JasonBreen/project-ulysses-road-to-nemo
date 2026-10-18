"""Move inherited country-history aircraft variants out of the active payload."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COUNTRY_DIR = ROOT / "mod" / "2985041246" / "history" / "countries"
ARCHIVE_DIR = ROOT / "inventory" / "inherited-legacy" / "history" / "countries"
FILES = (
    "BLK - Belka.txt",
    "FAT - FATO.txt",
    "GEB - Gebet.txt",
    "OSE - Osea.txt",
    "SAP - Sapin.txt",
    "UST - Ustio.txt",
)
START = re.compile(r"(?m)^[ \t]*create_equipment_variant\s*=\s*\{")


def block_end(text: str, start: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                end = index + 1
                if end < len(text) and text[end] == "\r":
                    end += 1
                if end < len(text) and text[end] == "\n":
                    end += 1
                return end
    raise ValueError(f"Unclosed create_equipment_variant block at byte {start}")


def strip_variants(text: str) -> tuple[str, list[str]]:
    spans = []
    for match in START.finditer(text):
        spans.append((match.start(), block_end(text, match.start())))
    removed = [text[start:end] for start, end in spans]
    for start, end in reversed(spans):
        text = text[:start] + text[end:]
    return text, removed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    total = 0
    for name in FILES:
        path = COUNTRY_DIR / name
        original = path.read_bytes().decode("utf-8")
        updated, removed = strip_variants(original)
        if not removed:
            print(f"{name}: no active legacy variants")
            continue
        archive = ARCHIVE_DIR / f"{path.stem}.equipment_variants.txt"
        if archive.exists() and args.apply:
            raise FileExistsError(archive)
        total += len(removed)
        print(f"{path.relative_to(ROOT)}: {len(removed)} block(s)")
        if args.apply:
            archive.write_bytes(("\n".join(removed) + "\n").encode("utf-8"))
            path.write_bytes(updated.encode("utf-8"))
    print(f"Legacy equipment blocks found: {total}")
    if not args.apply and total:
        print("Dry run only; rerun with --apply to write changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
