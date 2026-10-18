"""Disable inherited pre-1.19 aircraft variants without deleting provenance.

The archive's By Blood Alone branches reference custom aircraft modules that
are not present in the installed 1.19 schema. The blocks stay in place for a
future migration, but a contradictory DLC limit prevents them from executing
while the continuation uses vanilla equipment definitions.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COUNTRY_DIR = ROOT / "mod" / "2985041246" / "history" / "countries"
PATTERN = re.compile(
    rb"(if\s*=\s*\{\s*limit\s*=\s*\{\s*has_dlc\s*=\s*\"By Blood Alone\"\s*)(\}\s*create_equipment_variant)",
    re.S,
)


def transform(data: bytes) -> tuple[bytes, int]:
    replacement = rb"\1NOT = { has_dlc = \"By Blood Alone\" }\r\n\t\2"
    return PATTERN.subn(replacement, data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write the guarded files")
    args = parser.parse_args()

    changed = 0
    for path in sorted(COUNTRY_DIR.glob("*.txt")):
        original = path.read_bytes()
        updated, count = transform(original)
        if not count:
            continue
        changed += count
        print(f"{path.relative_to(ROOT)}: {count} legacy branch(es)")
        if args.apply:
            path.write_bytes(updated)
    print(f"Legacy equipment branches found: {changed}")
    if not args.apply and changed:
        print("Dry run only; rerun with --apply to write changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
