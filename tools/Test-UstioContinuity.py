#!/usr/bin/env python3
"""Offline contract checks for the repaired inherited Ustio scaffold."""

from __future__ import annotations

import argparse
import re
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


def focus_block(text: str, focus_id: str) -> str:
    match = re.search(
        rf"(?m)^shared_focus = \{{\s*\n\s*id = {re.escape(focus_id)}(?:\s|$)",
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


def assert_focus_coordinate(text: str, focus_id: str, expected_x: int) -> None:
    block = focus_block(text, focus_id)
    require(block, f"focus block is missing: {focus_id}")
    coordinate = re.search(r"(?m)^\s*x\s*=\s*(-?\d+)\s*$", block)
    require(coordinate is not None, f"focus coordinate is missing: {focus_id}")
    require(int(coordinate.group(1)) == expected_x, f"unexpected x coordinate for {focus_id}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mod-root", type=Path, default=ROOT / "mod" / "2985041246")
    args = parser.parse_args()
    mod_root = args.mod_root.resolve()

    focus_tree = read(mod_root, "common/national_focus/UST.txt")
    shared_focus = read(mod_root, "common/national_focus/UST_shared.txt")
    continuation = read(mod_root, "events/ac_continuation.txt")
    ustio = read(mod_root, "events/ac_ustio_continuation.txt")
    legacy_ustio = read(mod_root, "events/Ustio.txt")
    default_ai = read(mod_root, "common/ai_strategy/default.txt")
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
    assert_focus_coordinate(shared_focus, "UST_to_modernise_fully", -1)
    mutated_focus = focus_block(shared_focus, "UST_to_modernise_fully").replace("x = -1", "x = 999", 1)
    mutated_source = shared_focus.replace(focus_block(shared_focus, "UST_to_modernise_fully"), mutated_focus, 1)
    try:
        assert_focus_coordinate(mutated_source, "UST_to_modernise_fully", -1)
    except AssertionError:
        pass
    else:
        raise AssertionError("focus-specific coordinate mutation was accepted")

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
    guarded_dispatches = re.findall(
        r"limit = \{ country_exists = UST \}\s*UST = \{\s*country_event = \{ id = ac_ustio\.1 days = 7 \}",
        continuation,
    )
    require(len(guarded_dispatches) == 3, "every Ustio dispatch must be guarded by country_exists = UST")
    require("belka_dlp_war.102" in continuation, "annexation guard is not documented at the conventional victory handoff")
    require("target = UST" in legacy_ustio, "Ustio opinion target must use the uppercase country tag")
    require("target = ust" not in legacy_ustio, "lowercase Ustio country tag remains")
    require("id = cv_nav_bomber" in default_ai, "default AI uses the obsolete air_cv_naval_bomber identifier")
    require("id = air_cv_naval_bomber" not in default_ai, "obsolete air_cv_naval_bomber identifier remains")

    handoff = event_block(ustio, "ac_ustio.1")
    require(handoff, "Ustio continuation event is missing")
    for token in (
        "has_global_flag = ac_postwar_contract_started",
        "NOT = { has_country_flag = ac_ustio_continuation_started }",
        "tree = ustio_democracy keep_completed = yes",
        "tree = ustio_non_ali keep_completed = yes",
    ):
        require(token in handoff, f"Ustio handoff lacks {token}")
    # The one-shot guard may only be consumed once a Ratio outcome exists, and
    # the no-outcome path must not reload a tree (ustio.1 can still resolve later).
    for flag in ("UST_sold_land_to_ratio_flag", "UST_not_sold_land_to_ratio_flag"):
        require(
            re.search(
                rf"limit = \{{.*?has_country_flag = {flag}.*?set_country_flag = ac_ustio_continuation_started",
                handoff,
                re.DOTALL,
            )
            is not None,
            f"handoff guard is not tied to {flag}",
        )
    non_ali_branch = re.search(
        r"else_if\s*=\s*\{\s*limit = \{(?P<body>.*?)\}\s*"
        r"set_country_flag = ac_ustio_continuation_started\s*"
        r"load_focus_tree = \{ tree = ustio_non_ali",
        handoff,
        re.DOTALL,
    )
    require(non_ali_branch is not None, "non-aligned handoff branch is missing")
    require(
        "NOT = { has_country_flag = UST_lost_ratio_war_flag }" in non_ali_branch.group("body"),
        "lost-Ratio-war outcome may reload the non-aligned Ustio tree",
    )
    require(handoff.count("set_country_flag = ac_ustio_continuation_started") == 2, "handoff guard is set outside the Ratio branches")
    require("tree = ustio_start" not in handoff and "else = {" not in handoff, "no-outcome handoff must stay retryable")
    require(
        re.search(r"(?m)^\s*country_event\s*=\s*\{\s*id\s*=\s*ustio\.1\b", read(mod_root, "events/Belka.txt")) is not None,
        "belka.9 no longer schedules the Ratio choice event ustio.1",
    )

    for key in ("ac_ustio.1.t", "ac_ustio.1.d", "ac_ustio.1.a"):
        # The reference validator only indexes versioned `key:0 "..."` entries.
        require(
            re.search(rf'(?m)^\s*{re.escape(key)}:\d+\s+"[^"]+"', localization) is not None,
            f"Ustio localization key missing or unversioned: {key}",
        )

    print("Ustio continuity regressions passed: restored scaffold, repaired coordinate, guarded handoff, and localization.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
