#!/usr/bin/env python3
"""Offline regression checks for the HOI4 1.19 native-compatibility port."""

from __future__ import annotations

import argparse
import importlib.util
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TECH_FOLDER_ROW_LIMIT = 40
# Vanilla 1.19 infantry_folder ends at @1946 = row 20; compatibility nodes go below it.
VANILLA_INFANTRY_LAST_ROW = 20


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def braced_block(text: str, start: int) -> str:
    opening = text.find("{", start)
    depth = 0
    for index in range(opening, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    return ""


def load_mapper():
    spec = importlib.util.spec_from_file_location("port_mapper", ROOT / "tools" / "Port-NativeEquipmentReferences.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def defined_technologies(mod_root: Path) -> set[str]:
    ids: set[str] = set()
    for path in (mod_root / "common" / "technologies").glob("*.txt"):
        ids.update(re.findall(r"(?m)^\t(\w+)\s*=\s*\{", read(path)))
    return ids


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mod-root", type=Path, default=ROOT / "mod" / "2985041246")
    args = parser.parse_args()
    mod_root = args.mod_root.resolve()

    # The mapper must not rewrite IDs the active technology overrides still define.
    mapper = load_mapper()
    still_defined = sorted(set(mapper.REPLACEMENTS) & defined_technologies(mod_root) - {"infantry_manpats"})
    require(not still_defined, f"mapper rewrites actively defined technologies: {still_defined}")
    require(mapper.REPLACEMENTS.get("antiair_1") == "interwar_antiair", "antiair_1 must map to the land anti-air technology")

    # Division-name groups used by Osea OOBs must be defined in the active payload.
    names = "".join(read(p) for p in (mod_root / "common" / "units" / "names_divisions").glob("*.txt"))
    defined_groups = set(re.findall(r"(?m)^(\w+)\s*=", names))
    used_groups: set[str] = set()
    for path in (mod_root / "history" / "units").glob("OSE_*.txt"):
        used_groups.update(re.findall(r"division_names_group\s*=\s*(\w+)", read(path)))
    missing = sorted(used_groups - defined_groups)
    require(not missing, f"Osea OOBs use undefined division-name groups: {missing}")

    # Compatibility technologies use folder grid rows, not research years.
    compat = read(mod_root / "common" / "technologies" / "ac_native_compatibility.txt")
    rows = [int(value) for value in re.findall(r"position\s*=\s*\{\s*x\s*=\s*-?\d+\s+y\s*=\s*(-?\d+)", compat)]
    require(len(rows) == 3, "expected three compatibility technology positions")
    require(all(VANILLA_INFANTRY_LAST_ROW < row <= TECH_FOLDER_ROW_LIMIT for row in rows), f"compatibility tech rows overlap the vanilla infantry tree or leave the folder: {rows}")

    # Sapin's IFV production idea must not list an equipment key twice.
    sapin = read(mod_root / "common" / "ideas" / "sapin.txt")
    idea = re.search(r"(?m)^\s*sap_concentrated_ifv_production\s*=\s*\{", sapin)
    require(idea is not None, "sap_concentrated_ifv_production is missing")
    idea_block = braced_block(sapin, idea.start())
    match = re.search(r"equipment_bonus\s*=\s*\{", idea_block)
    require(match is not None, "Sapin IFV equipment bonus is missing")
    bonus = braced_block(idea_block, match.start())
    keys = re.findall(r"(?m)^\s*(\w+)\s*=\s*\{", bonus)[1:]
    require(len(keys) == len(set(keys)), f"duplicate equipment bonus keys: {keys}")
    require("armored_car_equipment" in keys, "IMV production bonus must target armored_car_equipment")
    # The archive's mot_rockets key meant motorized rocket systems, not towed rockets.
    artillery = re.search(r"(?m)^\s*sap_concentrated_artillery_production\s*=\s*\{", sapin)
    require(artillery is not None, "sap_concentrated_artillery_production is missing")
    artillery_block = braced_block(sapin, artillery.start())
    require("motorized_rocket_equipment = {" in artillery_block and "rocket_artillery_equipment" not in artillery_block,
            "artillery production idea must target motorized_rocket_equipment")

    # Ustio's MANPATS rewards must stock equipment usable by anti-tank battalions.
    ustio = read(mod_root / "common" / "national_focus" / "UST_shared.txt")
    for focus_id in ("UST_import_MANPATS", "UST_to_arm_the_man"):
        start = re.search(rf"(?m)^shared_focus = \{{\s*\n\s*id = {focus_id}\b", ustio)
        require(start is not None, f"{focus_id} is missing")
        block = braced_block(ustio, start.start())
        require("type = anti_tank_equipment_1" in block, f"{focus_id} does not stock anti-tank equipment")
    arm_the_man = braced_block(ustio, re.search(r"(?m)^shared_focus = \{\s*\n\s*id = UST_to_arm_the_man\b", ustio).start())
    stock = re.findall(r"type\s*=\s*(\w+)", arm_the_man)
    require(stock.count("anti_tank_equipment_1") == 1 and "support_equipment" in stock,
            f"UST_to_arm_the_man must keep one anti-tank and one support-equipment reward: {stock}")

    # sap_protecting_our_infantry's bonus targets the mod-defined cat_imvs category; the
    # quarantined armor tree held its other members, so imv1 must carry it.
    tech_text = "".join(read(p) for p in (mod_root / "common" / "technologies").glob("*.txt"))
    if "category = cat_imvs" in read(mod_root / "common" / "national_focus" / "SAP_pre_belkan_war.txt"):
        require(re.search(r"(?m)^\s*cat_imvs\s*$", tech_text), "cat_imvs research bonus has no active technology")

    # Visible compatibility technologies need names and descriptions.
    localization = "".join(read(p) for p in (mod_root / "localisation").rglob("*.yml"))
    for tech in re.findall(r"(?m)^\t(\w+)\s*=\s*\{", compat):
        for key in (tech, f"{tech}_desc"):
            require(re.search(rf'(?m)^\s*{key}:\d+\s+"[^"]+"', localization), f"compatibility tech localization missing: {key}")

    # Script-created advisor roles cannot carry triggers or effects in 1.19, so
    # the focus-unlocked Crown Regents keep their hire guard in the database role.
    characters = re.sub(r"#[^\n]*", "", read(mod_root / "common" / "characters" / "SAP.txt"))
    regents = ("SAP_alphonso_espinal", "SAP_domingo_escalona", "SAP_ramira_arguijo", "SAP_raul_de_haro")
    for regent, focus in (("SAP_alphonso_espinal", "sap_regent_alphonso_espinal"), ("SAP_domingo_escalona", "sap_regent_domingo_escalona")):
        start = re.search(rf"(?m)^\t{regent}\s*=\s*\{{", characters)
        require(start is not None, f"{regent} character is missing")
        role = braced_block(characters, start.start())
        available = re.search(r"available\s*=\s*\{", role)
        require(available is not None, f"{regent} database role has no available guard")
        guard = braced_block(role, available.start())
        require(f"has_completed_focus = {focus}" in guard, f"{regent} role is not unlocked by {focus}")
        for other in regents:
            if other != regent:
                require(other in guard, f"{regent} role does not exclude {other}")
        require("on_add" in role, f"{regent} role lost its power-balance on_add")
    sapin_focus = read(mod_root / "common" / "national_focus" / "SAP_pre_belkan_war.txt")
    for regent in ("SAP_alphonso_espinal", "SAP_domingo_escalona"):
        require(f"character = {regent}" not in sapin_focus, f"{regent} is still added through an unguarded script role")

    # SAP_court_moderate_support: the else branch must be a sibling of its if.
    decisions = read(mod_root / "common" / "decisions" / "SAP_decisions.txt")
    decision = re.search(r"(?m)^\s*SAP_court_moderate_support\s*=\s*\{", decisions)
    require(decision is not None, "SAP_court_moderate_support is missing")
    complete = braced_block(decisions, decisions.find("complete_effect", decision.start()))
    depth = 0
    depths = {}
    for token in re.finditer(r"\{|\}|\b(if|else)\s*=", complete):
        if token.group(0) == "{":
            depth += 1
        elif token.group(0) == "}":
            depth -= 1
        else:
            depths.setdefault(token.group(1), depth)
    require(depths.get("if") is not None and depths.get("if") == depths.get("else"), "SAP_court_moderate_support else is nested inside its if")

    # infantry_weapons1 is a native 1.19 tech (infantry_equipment_1) and must keep its grants.
    require("infantry_weapons1" not in mapper.REPLACEMENTS, "mapper rewrites the native infantry_weapons1 technology")
    histories = {p.name: read(p) for p in (mod_root / "history" / "countries").glob("*.txt")}
    require(
        any(re.search(r"(?m)^\s*infantry_weapons1\s*=\s*1", text) for text in histories.values()),
        "no country history grants infantry_weapons1",
    )

    # The archive's own By Blood Alone aa_lmg grants unlock the light MG modules those
    # countries' designer aircraft use; only the separate antiair_1 grant maps to land AA.
    for tag in ("BLK", "FAT", "GEB", "OSE", "SAP", "UST"):
        history = next((text for name, text in histories.items() if name.startswith(f"{tag} ")), "")
        require(re.search(r"(?m)^\s*aa_lmg\s*=\s*1", history), f"{tag} lost its By Blood Alone aa_lmg grant")

    # ifv1/imv1 are the only unlocks for the custom ifv/imv battalions in starting OOBs
    # (set_oob in country history; event-loaded OOBs are outside this contract).
    for unit, tech in (("ifv", "ifv1"), ("imv", "imv1")):
        for name, history in histories.items():
            for oob in set(re.findall(r'(?m)^\s*set_oob\s*=\s*"?(\w+)"?', re.sub(r"#[^\n]*", "", history))):
                path = mod_root / "history" / "units" / f"{oob}.txt"
                if not path.exists() or not re.search(rf"(?m)^\s*{unit}\s*=\s*\{{", re.sub(r"#[^\n]*", "", read(path))):
                    continue
                require(re.search(rf"(?m)^\s*{tech}\s*=\s*1", history), f"{name[:3]} OOB {path.name} uses {unit} but history lacks {tech}")

    # BLK and OSE are mod-only tags, so their unit/ship name pools must stay active,
    # keyed only by 1.19 types (no pre-By Blood Alone aircraft archetypes).
    legacy_air_keys = ("fighter_equipment", "CAS_equipment", "nav_bomber_equipment", "cv_fighter_equipment",
                       "cv_CAS_equipment", "cv_nav_bomber_equipment", "heavy_fighter_equipment",
                       "tac_bomber_equipment", "strat_bomber_equipment")
    for tag in ("BLK", "OSE"):
        names_file = mod_root / "common" / "units" / "names" / f"00_{tag}_names.txt"
        require(names_file.exists(), f"{tag} unit name list is not active")
        names_text = re.sub(r"#[^\n]*", "", read(names_file))
        stale = [key for key in legacy_air_keys if re.search(rf"(?m)^\t{key}\s*=\s*\{{", names_text)]
        require(not stale, f"{tag} name list uses removed aircraft archetypes: {stale}")

    # Equipment variants keep their archive has_dlc wrappers and precede nothing unguarded:
    # a bare top-level block would load DLC-only and legacy designs in every configuration.
    for name, text in histories.items():
        code = re.sub(r"#[^\n]*", "", text)
        depth = 0
        for token in re.finditer(r"\{|\}|\bcreate_equipment_variant\s*=", code):
            if token.group(0) == "{":
                depth += 1
            elif token.group(0) == "}":
                depth -= 1
            else:
                require(depth > 0, f"{name}: create_equipment_variant outside its has_dlc wrapper")
    referenced = set()
    for path in (mod_root / "history" / "units").glob("*.txt"):
        referenced.update(re.findall(r'\bversion_name\s*=\s*"([^"]+)"', read(path)))
    defined = set()
    # Some designs (e.g. BLK's "Placeholder Class" ships) are created by decisions.
    scripts = [read(p) for folder in ("common", "events", "history") for p in (mod_root / folder).rglob("*.txt")]
    for text in scripts:
        for match in re.finditer(r"create_equipment_variant\s*=\s*\{", text):
            variant = re.search(r'\bname\s*=\s*"([^"]+)"', braced_block(text, match.start()))
            if variant:
                defined.add(variant.group(1))
    missing_variants = sorted(referenced - defined)
    require(not missing_variants, f"OOBs reference undefined equipment variants: {missing_variants[:5]}")

    print(
        "Native compatibility contracts passed: mapper IDs, Osea division names, tech rows, Sapin bonus, "
        "MANPATS rewards, tech localization, regent guards, Sapin decision structure, infantry grants, "
        "BLK/OSE name lists, and variant DLC wrappers."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
