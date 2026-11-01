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


def named_block(text: str, identifier: str) -> str:
    match = re.search(rf"(?m)^\s*{re.escape(identifier)}\s*=\s*\{{", text)
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
                return text[match.start():index + 1]
    return ""


def focus_blocks(text: str) -> dict[str, str]:
    blocks: dict[str, str] = {}
    for match in re.finditer(r"(?m)^\s*shared_focus\s*=\s*\{", text):
        opening = text.find("{", match.start())
        depth = 0
        end = None
        for index in range(opening, len(text)):
            if text[index] == "{":
                depth += 1
            elif text[index] == "}":
                depth -= 1
                if depth == 0:
                    end = index + 1
                    break
        if end is None:
            continue
        block = text[match.start():end]
        focus_id = re.search(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_]+)", block)
        if focus_id:
            blocks[focus_id.group(1)] = block
    return blocks


def focus_tree_blocks(text: str) -> dict[str, str]:
    blocks: dict[str, str] = {}
    for match in re.finditer(r"(?m)^\s*focus_tree\s*=\s*\{", text):
        opening = text.find("{", match.start())
        depth = 0
        end = None
        for index in range(opening, len(text)):
            if text[index] == "{":
                depth += 1
            elif text[index] == "}":
                depth -= 1
                if depth == 0:
                    end = index + 1
                    break
        if end is None:
            continue
        block = text[match.start():end]
        tree_id = re.search(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_]+)", block)
        if tree_id:
            blocks[tree_id.group(1)] = block
    return blocks


def focus_positions(texts: list[str]) -> dict[str, tuple[int, int]]:
    blocks: dict[str, str] = {}
    for text in texts:
        blocks.update(focus_blocks(text))
    positions: dict[str, tuple[int, int]] = {}

    def resolve(focus_id: str, stack: set[str]) -> tuple[int, int]:
        if focus_id in positions:
            return positions[focus_id]
        if focus_id in stack or focus_id not in blocks:
            raise AssertionError(f"cannot resolve focus position for {focus_id}")
        block = blocks[focus_id]
        x_match = re.search(r"(?m)^\s*x\s*=\s*(-?\d+)", block)
        y_match = re.search(r"(?m)^\s*y\s*=\s*(-?\d+)", block)
        require(x_match is not None and y_match is not None, f"focus lacks coordinates: {focus_id}")
        x, y = int(x_match.group(1)), int(y_match.group(1))
        parent_match = re.search(r"(?m)^\s*relative_position_id\s*=\s*([A-Za-z0-9_]+)", block)
        if parent_match:
            px, py = resolve(parent_match.group(1), stack | {focus_id})
            x, y = px + x, py + y
        positions[focus_id] = (x, y)
        return x, y

    for focus_id in blocks:
        resolve(focus_id, set())
    return positions


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    belka_events = read("events/Belka.txt")
    world_events = read("events/ac_world_events.txt")
    continuation = read("events/ac_continuation.txt")
    focus = read("common/national_focus/ac_belkan_campaign.txt")
    focus_trees = read("common/national_focus/BLK.txt")
    inherited_focus = read("common/national_focus/BLK_start.txt")
    decisions = read("common/decisions/ac_belkan_campaign.txt")
    campaign_effects = read("common/scripted_effects/ac_campaign_effects.txt")
    continuation_decisions = read("common/decisions/ac_continuation_decisions.txt")
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

    trees = focus_tree_blocks(focus_trees)
    for tree_id in ("belka_start", "belka_dlp_pre_war"):
        require(tree_id in trees, f"Belkan focus tree is missing: {tree_id}")
        require(
            trees[tree_id].count("shared_focus = ac_belkan_prewar_briefing") == 1,
            f"{tree_id} does not expose exactly one stable campaign opening",
        )

    opening_focus = focus_blocks(focus)["ac_belkan_prewar_briefing"]
    opening_ai = named_block(opening_focus, "ai_will_do")
    opening_available = named_block(opening_focus, "available")
    require("factor = 100" in opening_ai, "campaign opening lost its post-election AI priority")
    require("factor = 0" in opening_ai, "campaign opening does not suppress pre-election AI selection")
    require(
        "NOT = { has_country_flag = BLK_DLP_won_flag }" in opening_ai,
        "campaign opening AI suppression is not tied to the DLP election result",
    )
    require("date" not in opening_available, "campaign opening was calendar-locked for human players")

    council = named_block(decisions, "ac_belkan_war_council")
    council_complete = named_block(council, "complete_effect")
    council_available = named_block(council, "available")
    require("ac_commit_belkan_war_campaign = yes" in council_complete, "War Council bypasses the shared commitment effect")
    require("set_country_flag = ac_campaign_war_committed" not in council_complete, "War Council duplicates the shared commitment flags")
    require("country_event = { id = belka_dlp_war.1" not in council_complete, "War Council dispatches the start event directly")
    require("ai_will_do = { base = 0 }" in council, "historical AI can still take the early War Council decision")
    require(council.count("NOT = { has_country_flag = ac_campaign_war_committed }") >= 2, "War Council remains visible or available after commitment")
    require("date" not in council_available, "War Council was calendar-locked for human players")

    commit = named_block(campaign_effects, "ac_commit_belkan_war_campaign")
    for token in (
        "original_tag = BLK",
        "NOT = { has_country_flag = ac_campaign_war_committed }",
        "NOT = { has_country_flag = ac_postwar_ready }",
        "NOT = { has_active_mission = BLK_war_start_timer_dec }",
        "NOT = { has_global_flag = ac_campaign_arc_started }",
        "NOT = { has_global_flag = belkan_war_is_happening }",
        "NOT = { has_global_flag = belka_won_belkan_war }",
        "NOT = { has_global_flag = belka_lost_belkan_war }",
        "NOT = { has_global_flag = belka_won_belkan_war_wacht_am_wal }",
        "set_country_flag = ac_campaign_war_committed",
        "set_global_flag = ac_campaign_arc_started",
        "set_variable = { ac_campaign_war_weeks = 0 }",
        "country_event = { id = belka_dlp_war.1 days = 1 }",
    ):
        require(token in commit, f"shared Belkan commitment effect lost contract token: {token}")
    for token in (
        "set_country_flag = ac_campaign_war_committed",
        "set_global_flag = ac_campaign_arc_started",
        "set_variable = { ac_campaign_war_weeks = 0 }",
        "country_event = { id = belka_dlp_war.1 days = 1 }",
    ):
        require(commit.count(token) == 1, f"shared Belkan commitment effect no longer applies exactly once: {token}")
    require("set_global_flag = belka_won_belkan_war" not in commit, "shared commitment effect scripts a war winner")

    legacy_start = event_block(world_events, "world_event.1")
    require("BLK = { ac_commit_belkan_war_campaign = yes }" in legacy_start, "historical start bypasses the shared commitment effect")
    require("country_event = { id = belka_dlp_war.1" not in legacy_start, "historical start still dispatches the Belkan start event directly")
    for token in (
        "news_event = { id = ac_news_event.10 days = 1 }",
        "UST = { country_event = { id = ustio.18 }}",
        "UST = {  country_event = { id = ustio.17 days = 2 }}",
    ):
        require(token in legacy_start, f"historical start lost an inherited notification: {token}")
    for outcome_flag in ("belka_won_belkan_war", "belka_lost_belkan_war", "belka_won_belkan_war_wacht_am_wal"):
        require(
            f"set_global_flag = {outcome_flag}" not in legacy_start,
            f"historical start now scripts an AI winner: {outcome_flag}",
        )

    require(
        "later preparation is not granted retroactively" in localization,
        "War Council localization does not warn players about natural early-war risk",
    )
    require("NOT = { has_decision = ac_belkan_civilian_reserve }" in decisions, "logistics decision is not mutually exclusive")
    require("NOT = { has_decision = ac_belkan_logistics_requisition }" in decisions, "civilian-reserve decision is not mutually exclusive")
    for decision_id in ("ac_belkan_logistics_requisition", "ac_belkan_civilian_reserve"):
        opening_decision = named_block(decisions, decision_id)
        require(opening_decision, f"{decision_id} is missing")
        require(
            opening_decision.count("NOT = { has_country_flag = ac_campaign_stage_one_pending }") >= 2,
            f"{decision_id} can reopen during the delayed stage-one dispatch",
        )
    require(all(token in weekly for token in ("ac_campaign_war_weeks > 18", "ac_campaign_war_weeks > 22", "ac_campaign_war_weeks > 26")), "AI fallback thresholds are not stage-relative")
    require(not re.search(r"ai_will_do\s*=\s*\{\s*base\s*=", focus), "focus AI weights still use decision syntax")

    campaign_events = read("events/ac_belkan_campaign.txt")
    for event_id in ("ac_campaign.20", "ac_campaign.21", "ac_campaign.22", "ac_campaign.23"):
        require("has_global_flag = belkan_war_is_happening" in event_block(campaign_events, event_id), f"{event_id} can apply stage effects after the war ends")
    for event_id, stage_flag, pending_flag in (
        ("ac_campaign.20", "ac_campaign_stage_one", "ac_campaign_stage_one_pending"),
        ("ac_campaign.21", "ac_campaign_stage_one", "ac_campaign_stage_one_pending"),
        ("ac_campaign.22", "ac_campaign_stage_two", "ac_campaign_stage_two_pending"),
        ("ac_campaign.23", "ac_campaign_stage_three", "ac_campaign_stage_three_pending"),
    ):
        block = event_block(campaign_events, event_id)
        require("set_variable = { ac_campaign_war_weeks = 0 }" in block, f"{event_id} does not reset stage timing")
        require(f"NOT = {{ has_country_flag = {stage_flag} }}" in block, f"{event_id} is not idempotently guarded")
        require(f"NOT = {{ has_country_flag = ac_postwar_ready }}" in block, f"{event_id} can mutate a postwar handoff")
        require(f"clr_country_flag = {pending_flag}" in block, f"{event_id} does not clear its pending lock")
    for decision_id, event_id, pending_flag in (
        ("ac_belkan_logistics_requisition", "ac_campaign.20", "ac_campaign_stage_one_pending"),
        ("ac_belkan_civilian_reserve", "ac_campaign.21", "ac_campaign_stage_one_pending"),
        ("ac_belkan_front_command", "ac_campaign.22", "ac_campaign_stage_two_pending"),
        ("ac_belkan_endurance_program", "ac_campaign.23", "ac_campaign_stage_three_pending"),
    ):
        complete = named_block(named_block(decisions, decision_id), "complete_effect")
        require(f"country_event = {{ id = {event_id} days = 1 }}" in complete, f"{decision_id} no longer dispatches its stage event")
        require(f"set_country_flag = {pending_flag}" in complete, f"{decision_id} does not lock the transition before dispatch")
        require(not re.search(r"set_country_flag = ac_campaign_stage_(?:one|two|three)(?:\s|$)", complete) and "add_ideas = ac_war_" not in complete, f"{decision_id} duplicates stage effects before its guarded event")

    require("ac_postwar_continuation = {" in categories, "postwar continuation category is missing")
    require("ac_postwar_local_settlement = {" in categories, "local settlement category is missing")
    require("ac_clear_belkan_campaign_ideas = yes" in continuation, "postwar handoff does not clear wartime ideas")
    require("remove_ideas = ac_postwar_unclassified_settlement" in continuation, "neutral settlement does not clear its penalty")
    require("ac_continuation.1.e" in localization and "ac_continuation.1.d" in localization, "continuation event description/option keys are not distinct")
    require("ac_postwar_demobilization = {" in continuation_decisions, "stable demobilization decision ID was removed")
    require("id = ac_postwar_demobilization" in focus and "shared_focus = ac_postwar_demobilization" in focus, "stable demobilization focus ID was removed")

    positions = focus_positions([inherited_focus, focus])
    inherited_positions = {position for focus_id, position in positions.items() if focus_id.startswith("BLK_")}
    branch_ids = {
        "ac_belkan_prewar_briefing",
        "ac_belkan_industrial_mobilization",
        "ac_belkan_logistics_network",
        "ac_belkan_security_mandate",
    }
    branch_positions = {focus_id: positions[focus_id] for focus_id in branch_ids}
    require(positions["BLK_the_crisis_continues"] == (8, 0), "inherited focus anchor moved unexpectedly")
    require(branch_positions["ac_belkan_prewar_briefing"] == (17, 1), "campaign opening focus is not offset from its inherited prerequisite")
    require(len(set(branch_positions.values())) == len(branch_positions), "campaign focus branch contains overlapping nodes")
    require(not (set(branch_positions.values()) & inherited_positions), "campaign focus branch overlaps inherited Belka nodes")

    print("Campaign review regressions passed: chronology, layout, categories, locks, idempotent timing, cleanup, and localization.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
