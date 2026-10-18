"""Quarantine or explicitly port inherited country-history equipment variants.

The archive blocks were authored against an older HOI4 schema.  Referencing a
block from an OOB is not sufficient reason to reactivate it: its equipment type,
modules, and name group must first be translated to the native 1.19 contract.
"""

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

# Explicit native-port rules.  These are deliberately narrow: unknown legacy
# tokens remain quarantined instead of being guessed into the active payload.
TYPE_REPLACEMENTS = {
    "medium_plane_scout_plane_airframe_1": "medium_plane_scout_plane_airframe",
    "small_plane_cas_airframe_0": "small_plane_cas_airframe",
    "small_plane_cas_airframe_1": "small_plane_cas_airframe",
    "small_plane_naval_bomber_airframe_1": "small_plane_naval_bomber_airframe",
}
MODULE_REPLACEMENTS = {
    "qaam_1_1x": "rocket_rails",
    "sasm_1_1x": "rocket_rails",
    "saam_1_2x": "rocket_rails",
    "lagm_1_1x": "rocket_rails",
    "gun_pods_1_2x": "aircraft_cannon_1_2x",
    "unguided_bomb": "bomb_locks",
    "unguided_bomb_large": "large_bomb_bay",
    "awacs_radar": "air_ground_radar_1",
}
NAME_GROUP_REPLACEMENTS = {
    "GER_CA_HISTORICAL": "GER",
    "GER_BB_HISTORICAL": "GER",
    "GER_CL_HISTORICAL": "GER",
    "GER_DD_HISTORICAL": "GER",
    "GER_SS_HISTORICAL": "GER",
    "GER_TB_HISTORICAL": "GER",
    "USA_BB_HISTORICAL": "USA",
    "USA_CA_HISTORICAL": "USA",
    "USA_CL_HISTORICAL": "USA",
    "USA_CV_HISTORICAL": "USA",
    "USA_DD_HISTORICAL": "USA",
    "USA_MINELAYERS_HISTORICAL": "USA",
    "USA_SS_HISTORICAL": "USA",
}
UNSUPPORTED_MODULES = {
    "airframe_delta_wing",
    "airframe_flying_wing",
    "airframe_mod_canards",
    "airframe_mod_dihedral_wings",
    "airframe_mod_faceted_frame",
    "airframe_reverse_swept_wing",
    "airframe_straight_wing",
    "airframe_swept_wing",
    "stealth_coating_1_medium",
}
LEGACY_SHIP_TYPES = {
    "battleship_1",
    "carrier_2",
    "destroyer_1",
    "heavy_cruiser_1",
    "light_cruiser_1",
    "submarine_1",
}


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


def normalize_variant_block(block: str) -> str:
    """Apply only documented native-schema substitutions to one block."""
    type_match = re.search(r"(?m)^(\s*type\s*=\s*)([A-Za-z0-9_]+)", block)
    if type_match and type_match.group(2) in TYPE_REPLACEMENTS:
        block = block[: type_match.start(2)] + TYPE_REPLACEMENTS[type_match.group(2)] + block[type_match.end(2) :]

    lines: list[str] = []
    for line in block.splitlines(keepends=True):
        module_match = re.match(r"(\s*\w+\s*=\s*)([A-Za-z0-9_]+)(\s*(?:#.*)?\r?\n?)$", line)
        if module_match:
            key, value = module_match.group(1), module_match.group(2)
            if key.strip().startswith("special_type_slot") and value in UNSUPPORTED_MODULES:
                continue
            if key.strip().startswith("name_group") and value.startswith(("FAT_", "SAP_")):
                # No active native name pool exists for these tags; leaving the
                # field would make the variant fail at load time.
                continue
            if key.strip().startswith("name_group"):
                value = NAME_GROUP_REPLACEMENTS.get(value, value)
            value = MODULE_REPLACEMENTS.get(value, value)
            line = f"{key}{value}{module_match.group(3)}"
        line = re.sub(r"^( +)(\t+)", r"\2", line)
        if line.endswith("\r\n"):
            line = line[:-2].rstrip(" \t") + "\r\n"
        elif line.endswith("\n"):
            line = line[:-1].rstrip(" \t") + "\n"
        else:
            line = line.rstrip(" \t")
        lines.append(line)
    return "".join(lines)


def guard_for_block(block: str) -> str:
    type_match = re.search(r"(?m)^\s*type\s*=\s*([A-Za-z0-9_]+)", block)
    if not type_match:
        raise ValueError("Variant block has no type")
    equipment_type = type_match.group(1)
    if equipment_type.startswith("ship_hull_") or equipment_type in LEGACY_SHIP_TYPES:
        if equipment_type in LEGACY_SHIP_TYPES:
            return 'limit = { not = { has_dlc = "Man the Guns" } }'
        return 'limit = { has_dlc = "Man the Guns" }'
    return 'limit = { has_dlc = "By Blood Alone" }'


def guarded_blocks(blocks: list[str]) -> str:
    groups: dict[str, list[str]] = {}
    for block in blocks:
        normalized = normalize_variant_block(block)
        groups.setdefault(guard_for_block(normalized), []).append(normalized)
    chunks: list[str] = []
    for guard, group in groups.items():
        chunks.append("if = {\n\t" + guard + "\n" + "\n".join(indent_block(item, "\t") for item in group) + "\n}\n")
    return "\n".join(chunks)


def indent_block(block: str, prefix: str) -> str:
    return "\n".join(prefix + line if line else line for line in block.rstrip("\r\n").splitlines())


def replace_active_variants(target: Path, blocks: list[str], apply: bool) -> int:
    original = target.read_text(encoding="utf-8-sig")
    stripped, _ = strip_variants(original)
    rendered = stripped.rstrip() + "\n\n" + guarded_blocks(blocks)
    print(f"{target.name}: native-porting {len(blocks)} variant block(s)")
    if apply:
        with target.open("w", encoding="utf-8", newline="") as handle:
            handle.write(rendered.rstrip() + "\n")
    return len(blocks)


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
        blocks = [
            normalize_variant_block(block)
            for variant_name, block in variant_blocks(source.read_text(encoding="utf-8"))
            if variant_name in wanted
        ]
        if not blocks:
            print(f"{name}: no referenced archive variants selected")
            continue
        restored += replace_active_variants(target, blocks, apply)
    return restored


def normalize_active_variants(apply: bool) -> int:
    total = 0
    for name in FILES:
        target = COUNTRY_DIR / name
        blocks = [block for _, block in variant_blocks(target.read_text(encoding="utf-8-sig"))]
        if blocks:
            total += replace_active_variants(target, blocks, apply)
    return total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument(
        "--restore-referenced",
        action="store_true",
        help="native-port only variants requested by active unit OOBs",
    )
    parser.add_argument(
        "--normalize-active",
        action="store_true",
        help="native-port current active variant blocks and restore their DLC guards",
    )
    args = parser.parse_args()
    if args.restore_referenced:
        restored = restore_referenced_variants(args.apply)
        print(f"Referenced equipment blocks native-ported: {restored}")
        if not args.apply and restored:
            print("Dry run only; rerun with --restore-referenced --apply to write changes.")
        return 0
    if args.normalize_active:
        total = normalize_active_variants(args.apply)
        print(f"Active equipment blocks native-ported: {total}")
        if not args.apply and total:
            print("Dry run only; rerun with --normalize-active --apply to write changes.")
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
