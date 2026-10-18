#!/usr/bin/env python3
"""Static contract checks for the provisional Belkan campaign arc.

This is intentionally offline and dependency-free. It catches missing files,
localization drift, broken campaign references, duplicate local IDs, and
developer/workshop paths. It does not parse the HOI4 engine grammar and does
not claim native runtime compatibility.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


FOCUSES = {
    "ac_belkan_prewar_briefing", "ac_belkan_industrial_mobilization",
    "ac_belkan_logistics_network", "ac_belkan_security_mandate",
    "ac_belkan_ultimatum", "ac_belkan_council_mandate",
    "ac_postwar_reconstruction", "ac_postwar_recovery_budget",
    "ac_postwar_demobilization", "ac_postwar_victory_settlement",
    "ac_postwar_defeat_settlement", "ac_postwar_victory_legacy",
    "ac_postwar_unclassified_settlement", "ac_postwar_defeat_legacy",
    "ac_postwar_unclassified_legacy", "ac_belkan_postwar",
}
DECISIONS = {
    "ac_belkan_war_council", "ac_belkan_logistics_requisition",
    "ac_belkan_civilian_reserve", "ac_belkan_front_command",
    "ac_belkan_endurance_program", "ac_postwar_ratify_victory",
    "ac_postwar_demobilize_establishment",
}
CATEGORIES = {
    "ac_belkan_campaign", "ac_postwar_continuation", "ac_postwar_local_settlement",
}
IDEAS = {
    "ac_prewar_cabinet", "ac_industrial_preparations", "ac_frontline_logistics",
    "ac_security_mandate", "ac_war_supply_drive", "ac_war_civilian_reserve",
    "ac_war_front_command", "ac_war_endurance", "ac_postwar_civic_legacy",
    "ac_postwar_survivor_state", "ac_postwar_unclassified_settlement",
    "ac_postwar_unclassified_legacy", "ac_postwar_victory_settlement",
    "ac_postwar_wacht_settlement", "ac_postwar_defeat_settlement",
    "ac_postwar_reconstruction", "ac_postwar_occupation_burden",
    "ac_postwar_guarantor",
}
EVENTS = {f"ac_campaign.{number}" for number in (1, 2, 3, 4, 5, 6, 20, 21, 22, 23, 30, 31, 32, 33, 34, 35, 36)}
CONTINUATION_EVENTS = {"ac_continuation.1", "ac_continuation.2", "ac_continuation.10", "ac_continuation.11"}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def loc_keys(text: str) -> set[str]:
    return set(re.findall(r"^\s*([A-Za-z_][A-Za-z0-9_.]*)\s*:\s*\d+\s+\"", text, re.MULTILINE))


def loc_key_counts(text: str) -> Counter[str]:
    return Counter(re.findall(r"^\s*([A-Za-z_][A-Za-z0-9_.]*)\s*:\s*\d+\s+\"", text, re.MULTILINE))


def declared_ids(text: str, ids: set[str]) -> dict[str, int]:
    found: dict[str, int] = {}
    for line_no, line in enumerate(text.splitlines(), 1):
        for item in ids:
            if re.search(rf"\bid\s*=\s*{re.escape(item)}(?:\s|$)", line):
                found[item] = found.get(item, 0) + 1
    return found


def block_balance(text: str) -> int:
    cleaned = re.sub(r"#[^\n]*", "", text)
    cleaned = re.sub(r'"(?:\\.|[^"\\])*"', '""', cleaned)
    return cleaned.count("{") - cleaned.count("}")


def extract_block(text: str, marker: str) -> str:
    start = text.find(marker)
    if start < 0:
        return ""
    opening = text.find("{", start)
    if opening < 0:
        return ""
    depth = 0
    for index in range(opening, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[start:index + 1]
    return text[start:]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mod-root", type=Path, default=Path(__file__).resolve().parents[1] / "mod" / "2985041246")
    args = parser.parse_args()
    mod = args.mod_root.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    required = [
        mod / "common" / "national_focus" / "ac_belkan_campaign.txt",
        mod / "common" / "decisions" / "ac_belkan_campaign.txt",
        mod / "common" / "decisions" / "categories" / "ac_belkan_campaign.txt",
        mod / "common" / "ideas" / "ac_belkan_campaign.txt",
        mod / "events" / "ac_belkan_campaign.txt",
        mod / "localisation" / "english" / "ac_belkan_campaign_l_english.yml",
    ]
    continuation_required = [
        mod / "common" / "decisions" / "ac_continuation_decisions.txt",
        mod / "common" / "ideas" / "ac_continuation.txt",
        mod / "common" / "scripted_effects" / "ac_campaign_effects.txt",
        mod / "events" / "ac_continuation.txt",
        mod / "localisation" / "english" / "country_BLK_continuation_l_english.yml",
    ]
    all_required = required + continuation_required
    for path in all_required:
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(mod)}")

    texts = {path: read(path) for path in all_required if path.is_file()}
    for path, text in texts.items():
        if block_balance(text) != 0:
            errors.append(f"unbalanced braces: {path.relative_to(mod)}")
        lowered = text.lower()
        for forbidden in (".claude/worktrees", "workshop", "g:/", "g:\\\\", "c:/users/"):
            if forbidden in lowered:
                errors.append(f"developer/workshop path in {path.relative_to(mod)}: {forbidden}")

    focus_text = texts.get(required[0], "")
    decision_text = texts.get(required[1], "")
    continuation_decisions = mod / "common" / "decisions" / "ac_continuation_decisions.txt"
    continuation_text = texts.get(continuation_decisions, "")
    continuation_ideas = mod / "common" / "ideas" / "ac_continuation.txt"
    continuation_events = mod / "events" / "ac_continuation.txt"
    continuation_idea_text = texts.get(continuation_ideas, "")
    continuation_event_text = texts.get(continuation_events, "")
    idea_text = texts.get(required[3], "") + "\n" + continuation_idea_text
    event_text = texts.get(required[4], "") + "\n" + continuation_event_text
    continuation_loc = mod / "localisation" / "english" / "country_BLK_continuation_l_english.yml"
    loc_text = texts.get(required[5], "") + "\n" + texts.get(continuation_loc, "")
    loc = loc_keys(loc_text)

    # The focus-tree ID is declared once; shared-focus references are checked
    # separately by the expected localization contract.
    declared_focuses = declared_ids(focus_text, FOCUSES)
    for item in sorted(FOCUSES):
        if item not in declared_focuses:
            errors.append(f"focus not declared in campaign file: {item}")
        if declared_focuses.get(item, 0) > 1:
            errors.append(f"duplicate focus declaration: {item}")
    declared_ideas = re.findall(r"^\s*(ac_[A-Za-z0-9_]+)\s*=\s*\{", idea_text, re.MULTILINE)
    for item in sorted(IDEAS):
        count = declared_ideas.count(item)
        if count == 0:
            errors.append(f"idea not declared in campaign file: {item}")
        if count > 1:
            errors.append(f"duplicate idea declaration: {item}")

    for item in sorted(DECISIONS):
        if not re.search(rf"^\s*{re.escape(item)}\s*=\s*\{{", decision_text + "\n" + continuation_text, re.MULTILINE):
            errors.append(f"decision not declared in campaign file: {item}")

    category_text = texts.get(required[2], "")
    for item in sorted(CATEGORIES):
        if not re.search(rf"^\s*{re.escape(item)}\s*=\s*\{{", category_text, re.MULTILINE):
            errors.append(f"decision category not declared: {item}")
        if item not in loc:
            errors.append(f"decision category localization missing: {item}")

    for item in sorted(EVENTS | CONTINUATION_EVENTS):
        if len(re.findall(rf"^\s*id\s*=\s*{re.escape(item)}(?:\s|$)", event_text, re.MULTILINE)) != 1:
            errors.append(f"event declaration count is not one: {item}")

    for item in sorted((FOCUSES - {"ac_belkan_postwar"}) | DECISIONS | IDEAS):
        if item not in loc or f"{item}_desc" not in loc:
            errors.append(f"missing localization pair: {item}")
    if "ac_belkan_campaign" not in loc or "ac_belkan_campaign_desc" not in loc:
        errors.append("missing campaign decision category localization")
    for item in sorted(EVENTS):
        for suffix in ("t", "d", "a"):
            if f"{item}.{suffix}" not in loc:
                errors.append(f"missing event localization: {item}.{suffix}")
    for item in sorted(CONTINUATION_EVENTS):
        suffixes = ("t", "d", "a", "b", "c", "e") if item == "ac_continuation.1" else ("t", "d", "a")
        for suffix in suffixes:
            if f"{item}.{suffix}" not in loc:
                errors.append(f"missing continuation event localization: {item}.{suffix}")

    for key, count in sorted(loc_key_counts(loc_text).items()):
        if count > 1 and (key.startswith("ac_campaign.") or key.startswith("ac_continuation.") or key.startswith("ac_postwar_") or key.startswith("ac_belkan_")):
            errors.append(f"duplicate campaign localization key: {key}")

    if re.search(r"ai_will_do\s*=\s*\{\s*base\s*=", focus_text):
        errors.append("campaign focus AI weights must use factor, not base")
    for token in ("has_decision = ac_belkan_civilian_reserve", "has_decision = ac_belkan_logistics_requisition"):
        if token not in decision_text:
            errors.append(f"opening-stage mutual exclusion missing: {token}")
    weekly = mod / "common" / "on_actions" / "ac_on_weekly_on_action.txt"
    weekly_text = read(weekly) if weekly.is_file() else ""
    for token in ("ac_campaign_war_weeks", "ac_campaign.20", "ac_campaign.22", "ac_campaign.23"):
        if token not in weekly_text:
            errors.append(f"AI pacing hook missing from weekly on_action: {token}")
    for token in ("ac_campaign_war_weeks > 18", "ac_campaign_war_weeks > 24", "ac_campaign_war_weeks > 30"):
        if token not in weekly_text:
            errors.append(f"AI fallback timing guard missing: {token}")
    if "set_country_flag = ac_postwar_ready" not in continuation_event_text:
        errors.append("postwar handoff no longer sets ac_postwar_ready")
    if "load_focus_tree = { tree = ac_belkan_postwar" not in continuation_event_text:
        errors.append("postwar handoff no longer loads ac_belkan_postwar")
    for token in (
        "set_global_flag = ac_postwar_unclassified",
        "add_timed_idea = { idea = ac_postwar_unclassified_settlement",
        "has_global_flag = ac_postwar_unclassified",
        "has_global_flag = belka_won_belkan_war",
        "has_global_flag = belka_won_belkan_war_wacht_am_wal",
        "has_global_flag = belka_lost_belkan_war",
    ):
        if token not in continuation_event_text and token not in focus_text:
            errors.append(f"unclassified postwar fallback coverage missing: {token}")

    effects_text = texts.get(mod / "common" / "scripted_effects" / "ac_campaign_effects.txt", "")
    for token in ("ac_clear_belkan_campaign_ideas = yes", "ac_war_supply_drive", "ac_war_civilian_reserve", "ac_war_front_command", "ac_war_endurance"):
        if token not in continuation_event_text and token not in effects_text:
            errors.append(f"postwar campaign cleanup coverage missing: {token}")

    world_events = read(mod / "events" / "ac_world_events.txt") if (mod / "events" / "ac_world_events.txt").is_file() else ""
    belka_events = read(mod / "events" / "Belka.txt") if (mod / "events" / "Belka.txt").is_file() else ""
    lost_focus = read(mod / "common" / "national_focus" / "BLK_war_lost.txt") if (mod / "common" / "national_focus" / "BLK_war_lost.txt").is_file() else ""
    nuclear_block = extract_block(belka_events, "country_event = {\n\tid = belka_dlp_war.101")
    lost_event_block = extract_block(belka_events, "country_event = { #return of the king")
    for token, source in (
        ("set_global_flag = ac_postwar_wait_for_defeat_tree", nuclear_block),
        ("country_event = { id = world_event.2 days = 2 }", lost_event_block),
        ("clr_global_flag = ac_postwar_wait_for_defeat_tree", world_events),
    ):
        if token not in source:
            errors.append(f"inherited defeat-story handoff coverage missing: {token}")
    if "country_event = { id = world_event.2 days = 1 }" in nuclear_block:
        errors.append("nuclear ending still fires world_event.2 before the inherited defeat tree")

    all_new_files = all_required + [weekly, mod / "common" / "national_focus" / "BLK.txt"]
    for path in all_new_files:
        if path.is_file() and "TODO" in read(path):
            warnings.append(f"TODO marker in touched campaign file: {path.relative_to(mod)}")

    print(f"Campaign static contract: {len(errors)} error(s), {len(warnings)} warning(s)")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
