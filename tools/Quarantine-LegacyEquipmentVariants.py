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


def variant_blocks(text: str) -> list[tuple[str, str]]:
    blocks = []
    for match in START.finditer(text):
        end = block_end(text, match.start())
        block = text[match.start():end]
        name = re.search(r'(?m)^[ \t]*name\s*=\s*"([^"]+)"', block)
        if name:
            blocks.append((name.group(1), block))
    return blocks


def referenced_variant_names() -> dict[str, set[str]]:
    references: dict[str, set[str]] = {}
    for path in (COUNTRY_DIR.parent / "units").glob("*.txt"):
        tag = path.name[:3]
        names = {
            match.group(2)
            for match in re.finditer(
                r'\b(version_name|variant_name)\s*=\s*"([^"]+)"',
                path.read_text(encoding="utf-8-sig"),
            )
        }
        if names:
            references.setdefault(tag, set()).update(names)
    return references


def restore_referenced_variants(apply: bool) -> int:
    references = referenced_variant_names()
    restored = 0
    for name in FILES:
        tag = name[:3]
        wanted = references.get(tag, set())
        if not wanted:
            continue
        source = ARCHIVE_DIR / f"{Path(name).stem}.equipment_variants.txt"
        target = COUNTRY_DIR / name
        if not source.exists():
            print(f"{name}: archive missing for {sorted(wanted)}")
            continue
        existing = {
            variant_name
            for variant_name, _ in variant_blocks(target.read_text(encoding="utf-8"))
        }
        blocks = [
            block
            for variant_name, block in variant_blocks(source.read_text(encoding="utf-8"))
            if variant_name in wanted and variant_name not in existing
        ]
        if not blocks:
            print(f"{name}: referenced variants already active")
            continue
        restored += len(blocks)
        print(f"{name}: {len(blocks)} referenced variant block(s) are not active")
        if apply:
            # The archive files hold bare blocks without their has_dlc wrappers, so
            # appending them would create DLC-only and legacy designs unconditionally
            # after the OOB lines. Restore them inside their original wrappers (see the
            # pre-quarantine history at 4df1f0d), and port any 1.14 aircraft modules first.
            raise SystemExit(
                f"{name}: refusing to append bare variants; restore them inside their "
                "original has_dlc wrappers before set_air_oob/set_naval_oob."
            )
    return restored


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument(
        "--restore-referenced",
        action="store_true",
        help="restore only variants requested by active unit OOBs",
    )
    args = parser.parse_args()
    if args.restore_referenced:
        restored = restore_referenced_variants(args.apply)
        print(f"Referenced equipment blocks restored: {restored}")
        if not args.apply and restored:
            print("Dry run only; rerun with --restore-referenced --apply to write changes.")
        return 0
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
