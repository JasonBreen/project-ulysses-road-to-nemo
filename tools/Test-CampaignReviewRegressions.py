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
    inherited_focus = read("common/national_focus/BLK_start.txt")
    decisions = read("common/decisions/ac_belkan_campaign.txt")
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
    require(branch_positions["ac_belkan_prewar_briefing"] == (12, 1), "campaign opening focus is not offset from its inherited prerequisite")
    require(len(set(branch_positions.values())) == len(branch_positions), "campaign focus branch contains overlapping nodes")
    require(not (set(branch_positions.values()) & inherited_positions), "campaign focus branch overlaps inherited Belka nodes")

    print("Campaign review regressions passed: chronology, layout, categories, locks, idempotent timing, cleanup, and localization.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
