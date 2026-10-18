#!/usr/bin/env python3
"""Offline contract checks for the repaired inherited Ustio scaffold."""

from __future__ import annotations

import re
import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
def read(mod_root: Path, relative: str) -> str:
    return (mod_root / relative).read_text(encoding="utf-8-sig")


def event_block(text: str, event_id: str) -> str:
    match = re.search(
        rf"(?m)^country_event = \{{[^\n]*\n\s*id = {re.escape(event_id)}(?:\s|$)",
        text,
    )
    if match is None:
        return ""
    opening = text.find("{", match.start())
    depth = 0
    for index in range(opening, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[match.start() : index + 1]
    return ""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mod-root", type=Path, default=ROOT / "mod" / "2985041246")
    args = parser.parse_args()
    mod_root = args.mod_root.resolve()

    focus_tree = read(mod_root, "common/national_focus/UST.txt")
    shared_focus = read(mod_root, "common/national_focus/UST_shared.txt")
    continuation = read(mod_root, "events/ac_continuation.txt")
    ustio = read(mod_root, "events/ac_ustio_continuation.txt")
    localization = read(mod_root, "localisation/english/country_UST_l_english.yml")

    for focus_id in (
        "UST_start",
        "UST_tyran_industry",
        "UST_connect_miedzyrzecz",
        "UST_pay_for_museum",
        "UST_upgrade_schooling_system",
        "UST_ratio_military_bases",
        "UST_anti_partisant_training",
    ):
        require(
            re.search(rf"(?m)^\s*shared_focus = {focus_id}\s*$", focus_tree)
            is not None,
            f"initial Ustio tree does not expose {focus_id}",
        )

    require("x = -1experience_gain_factor" not in shared_focus, "corrupt Ustio focus coordinate remains")
    require("x = -1" in shared_focus, "repaired Ustio focus coordinate is missing")

    army_debate = re.search(
        r"(?ms)^shared_focus = \{\s*id = UST_army_debate.*?(?=^shared_focus = \{|\Z)",
        shared_focus,
    )
    require(army_debate is not None, "UST_army_debate definition is missing")
    require("has_global_flag = ac_postwar_contract_started" in army_debate.group(0), "army branch bypasses the postwar handoff gate")
    require("UST_sold_land_to_ratio_flag" in army_debate.group(0), "democracy handoff cannot reach UST_army_debate")
    require("UST_not_sold_land_to_ratio_flag" in army_debate.group(0), "non-aligned handoff cannot reach UST_army_debate")

    require("UST = {" in continuation and "id = ac_ustio.1" in continuation, "victory handoff does not dispatch Ustio")
    require(continuation.count("id = ac_ustio.1 days = 7") == 3, "only live Ustio settlement outcomes may dispatch Ustio")
    require("belka_dlp_war.102" in continuation, "annexation guard is not documented at the conventional victory handoff")

    handoff = event_block(ustio, "ac_ustio.1")
    require(handoff, "Ustio continuation event is missing")
    for token in (
        "has_global_flag = ac_postwar_contract_started",
        "NOT = { has_country_flag = ac_ustio_continuation_started }",
        "set_country_flag = ac_ustio_continuation_started",
        "tree = ustio_democracy keep_completed = yes",
        "tree = ustio_non_ali keep_completed = yes",
        "tree = ustio_start keep_completed = yes",
    ):
        require(token in handoff, f"Ustio handoff lacks {token}")

    for key in ("ac_ustio.1.t:", "ac_ustio.1.d:", "ac_ustio.1.a:"):
        require(key in localization, f"Ustio localization key missing: {key}")

    print("Ustio continuity regressions passed: restored scaffold, repaired coordinate, guarded handoff, and localization.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
