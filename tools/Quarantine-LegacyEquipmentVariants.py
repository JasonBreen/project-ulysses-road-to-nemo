"""Quarantine or explicitly port inherited country-history equipment variants.

The archive blocks were authored against an older HOI4 schema.  Referencing a
block from an OOB is not sufficient reason to reactivate it: its equipment type,
modules, and name group must first be translated to the native 1.19 contract.
"""

from __future__ import annotations

import argparse
import re
import textwrap
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
# Variant types must be concrete equipment, not archetypes. 1.19 generates
# medium_plane_scout_plane_airframe_1, small_plane_cas_airframe_1..3 and
# small_plane_naval_bomber_airframe_1..3 via for_each in x_plane_airframes.txt;
# there is no small_plane_cas_airframe_0. The archetype keys are mapped back so
# earlier normalized output is repaired on the next run.
TYPE_REPLACEMENTS = {
    "small_plane_cas_airframe_0": "small_plane_cas_airframe_1",
    "medium_plane_scout_plane_airframe": "medium_plane_scout_plane_airframe_1",
    "small_plane_cas_airframe": "small_plane_cas_airframe_1",
    "small_plane_naval_bomber_airframe": "small_plane_naval_bomber_airframe_1",
}
# OOB wings request a variant by equipment type and version_name, so the same
# type mapping must reach history/units or the names stop matching.
OOB_TYPE_REPLACEMENTS = {
    "small_plane_cas_airframe_0": "small_plane_cas_airframe_1",
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
    return relocate_slot_modules("".join(lines))


# Modules whose 1.19 category only fits special_type_slot_N; the main weapon slot
# then takes the vanilla scout-plane module (see generic_planes.txt AI designs).
SPECIAL_SLOT_ONLY_MODULES = {"air_ground_radar_1": "recon_camera"}


def relocate_slot_modules(block: str) -> str:
    for module, main_weapon in SPECIAL_SLOT_ONLY_MODULES.items():
        main = re.search(rf"(?m)^([ \t]*)fixed_main_weapon_slot\s*=\s*{module}\b[^\n]*\n?", block)
        if not main:
            continue
        used = set(re.findall(r"(?m)^\s*(special_type_slot_\d)\s*=", block))
        free = next((f"special_type_slot_{n}" for n in range(1, 5) if f"special_type_slot_{n}" not in used), None)
        if free is None:
            raise ValueError(f"No free special slot for {module}")
        indent = main.group(1)
        newline = "\r\n" if main.group(0).endswith("\r\n") else "\n"
        replacement = f"{indent}fixed_main_weapon_slot = {main_weapon}{newline}{indent}{free} = {module}{newline}"
        block = block[: main.start()] + replacement + block[main.end():]
    return fix_airframe_slots(block)


# 1.19 slot/category rules (common/units/equipment/plane_airframes.txt) that the
# blanket module mapping above cannot see, because they depend on the airframe:
# - small and carrier airframes take cas_weapon, not strat_weapon, in the
#   auxiliary slot, so the large bomb bay becomes bomb_locks;
# - carrier small airframes have only special_type_slot_1..2;
# - a medium airframe's main slot takes fighter/tac weapons only, so a CAS tank
#   buster moves to a free auxiliary slot behind an aircraft cannon;
# - large airframes take the large flying-boat hull, not the medium one.
SMALL_AIRFRAME = re.compile(r"^(?:cv_)?small_plane_")
SPECIAL_SLOT_COUNT = {"cv_small_plane_airframe": 2}


def set_module(block: str, slot: str, module: str) -> str:
    return re.sub(rf"(?m)^(\s*{slot}\s*=\s*)\w+", rf"\g<1>{module}", block, count=1)


def fix_airframe_slots(block: str) -> str:
    type_match = re.search(r"(?m)^\s*type\s*=\s*(\w+)", block)
    if not type_match:
        return block
    equipment = type_match.group(1)
    modules = dict(re.findall(r"(?m)^\s*(\w+_slot(?:_\d+)?)\s*=\s*(\w+)", block))

    if SMALL_AIRFRAME.match(equipment):
        for slot, module in modules.items():
            if slot.startswith("fixed_auxiliary_weapon_slot") and module == "large_bomb_bay":
                block = set_module(block, slot, "bomb_locks")

    family = re.sub(r"_\d+$", "", equipment)
    limit = SPECIAL_SLOT_COUNT.get(family)
    if limit:
        used = {int(n) for n in re.findall(r"(?m)^\s*special_type_slot_(\d+)\s*=", block)}
        for number in sorted(n for n in used if n > limit):
            free = next((n for n in range(1, limit + 1) if n not in used), None)
            if free is None:
                block = re.sub(rf"(?m)^[ \t]*special_type_slot_{number}\s*=[^\n]*\n?", "", block)
            else:
                block = re.sub(rf"(?m)^(\s*)special_type_slot_{number}(\s*=)", rf"\g<1>special_type_slot_{free}\2", block)
                used = (used - {number}) | {free}

    if family == "medium_plane_airframe" and modules.get("fixed_main_weapon_slot") == "tank_buster_1":
        used = set(modules)
        free = next((f"fixed_auxiliary_weapon_slot_{n}" for n in range(1, 4) if f"fixed_auxiliary_weapon_slot_{n}" not in used), None)
        if free is None:
            raise ValueError("No free auxiliary slot for tank_buster_1")
        main = re.search(r"(?m)^([ \t]*)fixed_main_weapon_slot\s*=\s*tank_buster_1[^\n]*(\r?\n)", block)
        indent, newline = main.group(1), main.group(2)
        block = (block[: main.start()] + f"{indent}fixed_main_weapon_slot = aircraft_cannon_1_2x{newline}"
                 f"{indent}{free} = tank_buster_1{newline}" + block[main.end():])

    if family.startswith("large_plane_"):
        for slot, module in modules.items():
            if slot.startswith("special_type_slot") and module == "flying_boat_medium":
                block = set_module(block, slot, "flying_boat_large")
    return block


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
    # Dedent first so re-running on already-wrapped blocks keeps one level.
    lines = textwrap.dedent(block.rstrip("\r\n").expandtabs(4)).splitlines()
    lines = [re.sub(r"^((?:    )+)", lambda m: "\t" * (len(m.group(1)) // 4), line) for line in lines]
    return "\n".join(prefix + line if line else line for line in lines)


# A top-level `if` left holding only its `limit` once its variants were stripped.
EMPTY_WRAPPER = re.compile(
    r"(?m)^if\s*=\s*\{\s*limit\s*=\s*\{(?:[^{}]|\{[^{}]*\})*\}\s*\}[ \t]*\r?\n?"
)


OOB_EFFECT = re.compile(r"\bset_(?:air|naval)_oob\b")


def first_oob_statement(text: str) -> int:
    """Start of the top-level statement that first loads an air or naval OOB."""
    match = OOB_EFFECT.search(text)
    if match is None:
        return len(text)
    depth = 0
    statement_start = 0
    index = 0
    while index < match.start():
        char = text[index]
        if char == "#":
            newline = text.find("\n", index)
            index = match.start() if newline < 0 else newline
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        elif char == "\n" and depth == 0:
            statement_start = index + 1
        index += 1
    return statement_start


def replace_active_variants(target: Path, blocks: list[str], apply: bool) -> int:
    original = target.read_text(encoding="utf-8-sig")
    stripped, _ = strip_variants(original)
    stripped = EMPTY_WRAPPER.sub("", stripped)
    # Variants must exist before the OOBs that request them by version_name.
    insert_at = first_oob_statement(stripped)
    head, tail = stripped[:insert_at].rstrip(), stripped[insert_at:]
    rendered = head + "\n\n" + guarded_blocks(blocks) + "\n" + tail
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
    rewrite_oob_types(apply)
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


def rewrite_oob_types(apply: bool) -> int:
    """Apply OOB_TYPE_REPLACEMENTS to unit OOBs as whole tokens."""
    changed = 0
    for path in sorted((COUNTRY_DIR.parent / "units").glob("*.txt")):
        raw = path.read_bytes()
        bom = raw.startswith(b"\xef\xbb\xbf")
        text = raw.decode("utf-8-sig")
        updated = text
        for old, new in OOB_TYPE_REPLACEMENTS.items():
            updated = re.sub(rf"(?<![A-Za-z0-9_]){re.escape(old)}(?![A-Za-z0-9_])", new, updated)
        if updated != text:
            changed += 1
            print(f"{path.name}: OOB equipment types ported")
            if apply:
                path.write_bytes((b"\xef\xbb\xbf" if bom else b"") + updated.encode("utf-8"))
    return changed


def normalize_active_variants(apply: bool) -> int:
    rewrite_oob_types(apply)
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
