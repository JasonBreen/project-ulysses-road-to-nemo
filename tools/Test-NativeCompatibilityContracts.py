#!/usr/bin/env python3
"""Offline regression checks for the HOI4 1.19 native-compatibility port."""

from __future__ import annotations

import argparse
import importlib.util
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TECH_FOLDER_ROW_LIMIT = 40


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
    still_defined = sorted(set(mapper.REPLACEMENTS) & defined_technologies(mod_root) - {"ifv1", "imv1", "infantry_manpats"})
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
    require(all(0 <= row <= TECH_FOLDER_ROW_LIMIT for row in rows), f"compatibility tech rows out of folder range: {rows}")

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

    # Ustio's MANPATS rewards must stock equipment usable by anti-tank battalions.
    ustio = read(mod_root / "common" / "national_focus" / "UST_shared.txt")
    for focus_id in ("UST_import_MANPATS", "UST_to_arm_the_man"):
        start = re.search(rf"(?m)^shared_focus = \{{\s*\n\s*id = {focus_id}\b", ustio)
        require(start is not None, f"{focus_id} is missing")
        block = braced_block(ustio, start.start())
        require("type = anti_tank_equipment_1" in block, f"{focus_id} does not stock anti-tank equipment")

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

    print(
        "Native compatibility contracts passed: mapper IDs, Osea division names, tech rows, Sapin bonus, "
        "MANPATS rewards, tech localization, regent guards, and Sapin decision structure."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
