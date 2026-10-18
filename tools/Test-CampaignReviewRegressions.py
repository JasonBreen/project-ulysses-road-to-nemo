#!/usr/bin/env python3
"""Focused offline regressions for the post-merge campaign review findings."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod" / "2985041246"


def read(relative: str) -> str:
    return (MOD / relative).read_text(encoding="utf-8-sig")


def event_block(text: str, event_id: str) -> str:
    match = re.search(rf"(?m)^country_event = \{{[^\n]*\n\s*id = {re.escape(event_id)}(?:\s|$)", text)
    if match is None:
        return ""
    start = match.start()
    opening = text.find("{", start)
    depth = 0
    for index in range(opening, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[start:index + 1]
    return ""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    belka_events = read("events/Belka.txt")
    world_events = read("events/ac_world_events.txt")
    continuation = read("events/ac_continuation.txt")
    focus = read("common/national_focus/ac_belkan_campaign.txt")
    decisions = read("common/decisions/ac_belkan_campaign.txt")
    categories = read("common/decisions/categories/ac_belkan_campaign.txt")
    weekly = read("common/on_actions/ac_on_weekly_on_action.txt")
    localization = "\n".join(
        (
            MOD / "localisation/english/ac_belkan_campaign_l_english.yml",
            MOD / "localisation/english/country_BLK_continuation_l_english.yml",
        )[i].read_text(encoding="utf-8-sig")
        for i in range(2)
    )

    nuclear = event_block(belka_events, "belka_dlp_war.101")
    lost = event_block(belka_events, "belka_dlp_lost.7")
    require("set_global_flag = ac_postwar_wait_for_defeat_tree" in nuclear, "nuclear branch lacks deferral flag")
    require("country_event = { id = world_event.2 days = 1 }" not in nuclear, "nuclear branch still dispatches continuation early")
    require("country_event = { id = world_event.2 days = 2 }" in lost, "final inherited defeat event no longer dispatches world_event.2")
    require("clr_global_flag = ac_postwar_wait_for_defeat_tree" in world_events, "world_event.2 does not clear deferral state")

    require("prerequisite = { focus = BLK_the_crisis_continues }" in focus, "campaign opening is not attached to the inherited prewar focus")
    require("NOT = { has_decision = ac_belkan_civilian_reserve }" in decisions, "logistics decision is not mutually exclusive")
    require("NOT = { has_decision = ac_belkan_logistics_requisition }" in decisions, "civilian-reserve decision is not mutually exclusive")
    require(all(token in weekly for token in ("ac_campaign_war_weeks > 18", "ac_campaign_war_weeks > 24", "ac_campaign_war_weeks > 30")), "AI fallback thresholds can race active decisions")
    require(not re.search(r"ai_will_do\s*=\s*\{\s*base\s*=", focus), "focus AI weights still use decision syntax")

    require("ac_postwar_continuation = {" in categories, "postwar continuation category is missing")
    require("ac_postwar_local_settlement = {" in categories, "local settlement category is missing")
    require("ac_clear_belkan_campaign_ideas = yes" in continuation, "postwar handoff does not clear wartime ideas")
    require("remove_ideas = ac_postwar_unclassified_settlement" in continuation, "neutral settlement does not clear its penalty")
    require("ac_continuation.1.e" in localization and "ac_continuation.1.d" in localization, "continuation event description/option keys are not distinct")

    print("Campaign review regressions passed: chronology, categories, locks, AI timing, cleanup, and localization.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
