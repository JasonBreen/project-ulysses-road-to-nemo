"""RETIRED: disable inherited pre-1.19 aircraft variants without deleting provenance.

The archive's By Blood Alone branches once referenced custom aircraft modules
absent from the installed 1.19 schema, and this tool made them unreachable with
a contradictory DLC limit. Those variants are now native-ported by
Quarantine-LegacyEquipmentVariants.py --normalize-active, and the BBA OOBs
request them by version_name, so applying this transform would disable valid
designs in every configuration. Only the dry-run report remains.
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
    if args.apply:
        raise SystemExit(
            "Retired: the BBA variant branches are native-ported; use "
            "Quarantine-LegacyEquipmentVariants.py --normalize-active instead."
        )

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
