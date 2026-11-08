"""Generate the Usea Depth minors B package: seven national trees and their contracts.

Sources: schema.py and the state modules in states/. Outputs are written whole;
--check is read-only and compares bytes. --validate TAG checks one state module
without writing anything (used while a state is being authored).

Static and offline only. Nothing here was tested in HOI4; native acceptance
remains under #8.
"""
import argparse
import importlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MOD = ROOT / "mod/2985041246"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools"))
from schema import ERAS, BANDS, F, E, O, I, R, D, L  # noqa: E402,F401
from usea_depth import seams  # noqa: E402

PKG = "minors_b"
NS = "ac_ud_minb"
ORDER = ("SYC", "CAL", "RJR", "ROH", "VOS", "CRS", "SHI")
EVENT_BASE = {"SYC": 100, "CAL": 200, "RJR": 300, "ROH": 400, "VOS": 500, "CRS": 600, "SHI": 700}
PLANNED = {"SYC": 60, "CAL": 60, "RJR": 60, "ROH": 60, "VOS": 60, "CRS": 60, "SHI": 30}
HEADER = "# Usea Depth minors B: provisional gameplay; owner: tools/usea_depth/minors_b/build.py.\n"
EVENT_PICTURES = {"air", "assembly", "bridge", "carrier", "communications", "diplomacy", "document", "economy", "gate",
                  "industry", "logistics", "medical", "missile", "navy", "peace", "radar", "rail", "refugees", "runway",
                  "satellite", "scales", "security", "shelter", "submarine", "tools"}
SLOT_BUILDINGS = {"industrial_complex", "arms_factory", "dockyard", "fuel_silo", "synthetic_refinery"}
BUILDINGS = SLOT_BUILDINGS | {"infrastructure", "air_base", "anti_air_building", "radar_station"}
RESOURCES = {"oil", "aluminium", "rubber", "tungsten", "steel", "chromium"}
IDEOLOGIES = {"democratic", "communism", "fascism", "neutrality", "monarchism"}
TECH = {"industry", "electronics", "naval_equipment", "infantry_weapons", "land_doctrine", "air_doctrine", "naval_doctrine",
        "construction_tech", "radar_tech", "logistics_tech", "artillery", "light_fighter", "synth_resources",
        "excavation_tech", "train_tech", "engineers_tech", "dd_tech", "ss_tech", "motorized_equipment", "naval_air"}
# Modifiers already used by the mod's own ideas; the package test re-reads that list.
MODIFIERS = {
    "stability_factor", "political_power_gain", "political_power_factor", "consumer_goods_factor", "war_support_factor",
    "production_factory_efficiency_gain_factor", "production_factory_max_efficiency_factor", "industrial_capacity_factory",
    "industrial_capacity_dockyard", "production_speed_buildings_factor", "production_speed_infrastructure_factor",
    "production_speed_industrial_complex_factor", "production_speed_arms_factory_factor", "production_speed_dockyard_factor",
    "production_speed_air_base_factor", "research_speed_factor", "local_resources_factor", "min_export", "trade_opinion_factor",
    "supply_consumption_factor", "army_core_defence_factor", "army_org_factor", "army_defence_factor", "army_morale_factor",
    "experience_gain_army_factor", "experience_gain_air_factor", "air_defence_factor", "air_superiority_efficiency",
    "air_intercept_efficiency", "air_detection", "naval_detection", "naval_coordination", "naval_speed_factor",
    "repair_speed_factor", "conscription_factor", "weekly_manpower", "monthly_population", "industry_repair_factor",
    "fuel_gain_factor", "static_anti_air_damage_factor", "dig_in_speed_factor", "max_dig_in_factor", "planning_speed",
    "drift_defence_factor", "democratic_drift", "communism_drift", "fascism_drift", "neutrality_drift",
    "opinion_gain_monthly_factor", "conversion_cost_civ_to_mil_factor", "conversion_cost_mil_to_civ_factor",
    "resistance_growth", "encryption_factor", "civilian_intel_to_others", "navy_org_factor", "naval_damage_factor",
    "naval_defense_factor", "mobilization_speed", "recruitable_population_factor", "production_speed_supply_node_factor",
    "army_speed_factor", "attrition", "org_loss_when_moving", "global_building_slots_factor", "party_popularity_stability_factor",
}
OUT = {}
LOC = {}
SCREEN = None


class Problem(Exception):
    pass


def tab(text, depth=1):
    return "".join(("\t" * depth + line if line else "") + "\n" for line in text.splitlines())


def block(key, body):
    return key + " = {\n" + tab(body) + "}\n"


def loc(key, text):
    text = text.replace('"', "'")
    if key in LOC and LOC[key] != text:
        raise Problem("Localisation conflict: " + key)
    LOC[key] = text


def load_state(tag):
    module = importlib.import_module("states." + tag.lower())
    importlib.reload(module)
    if module.TAG != tag:
        raise Problem(tag + ": module TAG is " + module.TAG)
    for name in ("FLAGS", "DECISIONS", "LEDGER"):
        if not hasattr(module, name):
            setattr(module, name, {} if name == "FLAGS" else [])
    return module


def fid(state, slug):
    return "%s_ud_%s" % (state.TAG, slug)


def idea_id(state, slug):
    return "%s_ud_%s_spirit" % (state.TAG, slug)


def decision_id(state, slug):
    return "%s_ud_%s_decision" % (state.TAG, slug)


def event_ids(state):
    return {e.slug: "%s.%d" % (NS, EVENT_BASE[state.TAG] + n) for n, e in enumerate(state.EVENTS, 1)}


def regime_name(state, slug):
    return "ac_ud_%s_regime_%s_%s" % (PKG, state.TAG.lower(), slug)


def office_id(state, regime):
    return "%s_ud_%s_office" % (state.TAG, regime.slug)


def tree_id(tag):
    return "ac_ud_%s_tree" % tag.lower()


def font20():
    text = (MOD / "gfx/fonts/ACBriefing20.fnt").read_text()
    return {int(c): int(a) for c, a in re.findall(r"char id=(\d+).*?xadvance=(\d+)", text)}


ADV20 = None


def title20(text):
    global ADV20
    if ADV20 is None:
        ADV20 = font20()
    return sum(ADV20.get(ord(c), 10) for c in text)


def title_fits(text):
    global SCREEN
    if SCREEN is None:
        SCREEN = seams._screen()
        SCREEN.metrics = SCREEN.font_metrics()[1]
    return len(SCREEN.wrapped_lines(text, 147, SCREEN.metrics)) <= 3 and all(
        sum(SCREEN.metrics.get(ord(c), 8) for c in line) <= 147 for line in SCREEN.wrapped_lines(text, 147, SCREEN.metrics))


# --- effect vocabulary -------------------------------------------------------

def owned(state_id, body, slot=None, level=1):
    condition = "is_owned_and_controlled_by = ROOT"
    if slot:
        condition += " free_building_slots = { building = %s size > %d include_locked = no }" % (slot, level - 1)
    return block("if", block("limit", "%s = { %s }" % (state_id, condition)) + block(str(state_id), body))


def expand(state, tokens, context, ideas, events):
    lines = []
    for token in tokens:
        kind, _, rest = token.partition(":")
        parts = rest.split(":")
        if kind == "idea":
            need(parts[0] in ideas, state, context, "unknown idea " + parts[0])
            lines.append("add_ideas = " + idea_id(state, parts[0]))
        elif kind == "swap":
            need(parts[0] in ideas and parts[1] in ideas, state, context, "unknown idea in " + token)
            old, new = idea_id(state, parts[0]), idea_id(state, parts[1])
            lines.append(block("if", block("limit", "has_idea = " + old) + "remove_ideas = " + old) + "add_ideas = " + new)
        elif kind == "remove":
            need(parts[0] in ideas, state, context, "unknown idea " + parts[0])
            lines.append("remove_ideas = " + idea_id(state, parts[0]))
        elif kind == "timed":
            need(parts[0] in ideas, state, context, "unknown idea " + parts[0])
            lines.append("add_timed_idea = { idea = %s days = %d }" % (idea_id(state, parts[0]), int(parts[1])))
        elif kind == "cap":
            lines.append("set_temp_variable = { ac_pol_capacity_delta = %d }\nac_pol_change_capacity = yes" % int(parts[0]))
        elif kind == "pp":
            lines.append("add_political_power = %d" % int(parts[0]))
        elif kind in ("stab", "ws"):
            value = float(parts[0])
            need(-0.15 <= value <= 0.15, state, context, "out-of-range " + token)
            lines.append("%s = %s" % ("add_stability" if kind == "stab" else "add_war_support", fmt(value)))
        elif kind == "xp":
            need(parts[0] in ("army", "navy", "air"), state, context, "bad experience " + token)
            lines.append("%s_experience = %d" % (parts[0], int(parts[1])))
        elif kind == "tech":
            need(parts[0] in TECH, state, context, "unreviewed tech category " + parts[0])
            need(context.startswith(state.TAG + "_ud_"), state, context, "tech bonuses belong to focuses")
            lines.append("add_tech_bonus = { name = %s bonus = %s uses = 1 category = %s }" % (context, fmt(float(parts[1])), parts[0]))
        elif kind == "build":
            state_id, building, level = int(parts[0]), parts[1], int(parts[2])
            need(building in BUILDINGS, state, context, "unreviewed building " + building)
            need(state_id in state.STATES, state, context, "state %d is not one of this country's mod states" % state_id)
            lines.append(owned(state_id, "add_building_construction = { type = %s level = %d instant_build = yes }" % (building, level),
                               building if building in SLOT_BUILDINGS else None, level))
        elif kind == "build_capital":
            building, level = parts[0], int(parts[1])
            need(building in BUILDINGS, state, context, "unreviewed building " + building)
            condition = "is_controlled_by = ROOT"
            if building in SLOT_BUILDINGS:
                condition += " free_building_slots = { building = %s size > %d include_locked = no }" % (building, level - 1)
            lines.append(block("capital_scope", block("if", block("limit", condition) +
                         "add_building_construction = { type = %s level = %d instant_build = yes }" % (building, level))))
        elif kind == "slots":
            state_id = int(parts[0])
            need(state_id in state.STATES, state, context, "state %d is not one of this country's mod states" % state_id)
            lines.append(block("if", block("limit", "%d = { is_owned_by = ROOT }" % state_id) +
                               "%d = { add_extra_state_shared_building_slots = %d }" % (state_id, int(parts[1]))))
        elif kind == "resource":
            state_id, resource, amount = int(parts[0]), parts[1], int(parts[2])
            need(state_id in state.STATES and resource in RESOURCES, state, context, "bad resource " + token)
            lines.append(block("if", block("limit", "%d = { is_owned_by = ROOT }" % state_id) +
                               "add_resource = { type = %s amount = %d state = %d }" % (resource, amount, state_id)))
        elif kind == "flag":
            need(parts[0] in state.FLAGS, state, context, "flag without a label: " + parts[0])
            lines.append("set_country_flag = " + fid(state, parts[0]))
        elif kind == "pop":
            need(parts[0] in IDEOLOGIES, state, context, "bad ideology " + parts[0])
            lines.append("add_popularity = { ideology = %s popularity = %s }" % (parts[0], fmt(float(parts[1]))))
        elif kind == "manpower":
            lines.append("add_manpower = %d" % int(parts[0]))
        elif kind == "event":
            need(parts[0] in events, state, context, "unknown event " + parts[0])
            lines.append("country_event = { id = %s days = 1 }" % events[parts[0]])
        elif kind == "regime":
            need(parts[0] in {r.slug for r in state.REGIMES}, state, context, "unknown regime " + parts[0])
            lines.append(regime_name(state, parts[0]) + " = yes")
        elif kind == "raw":
            need(not seams.banned_uses(rest), state, context, "banned effect in raw script")
            lines.append(rest)
        else:
            raise Problem("%s %s: unknown effect token %s" % (state.TAG, context, token))
    return "\n".join(lines)


def fmt(value):
    return ("%.3f" % value).rstrip("0").rstrip(".")


PROBLEMS = []


def need(condition, state, context, message):
    if not condition:
        PROBLEMS.append("%s %s: %s" % (state.TAG, context, message))


def reaches_regime(tokens):
    return any(t.startswith("regime:") for t in tokens)


# --- validation --------------------------------------------------------------

def validate(state):
    """Structural, layout, text and political checks for one state module."""
    tag = state.TAG
    slugs = [f.slug for f in state.FOCUSES]
    need(len(slugs) == len(set(slugs)), state, "focuses", "duplicate focus slug")
    need(abs(len(slugs) - PLANNED[tag]) <= 6, state, "focuses", "expected about %d focuses, found %d" % (PLANNED[tag], len(slugs)))
    by = {f.slug: f for f in state.FOCUSES}
    ideas = {i.slug for i in state.IDEAS}
    events = event_ids(state)
    need(len(ideas) == len(state.IDEAS), state, "ideas", "duplicate idea slug")
    need(len(events) == len(state.EVENTS), state, "events", "duplicate event slug")
    need(2 <= len(state.REGIMES) <= 3, state, "regimes", "two or three political paths are required")
    rows = {}
    for f in state.FOCUSES:
        context = fid(state, f.slug)
        need(re.fullmatch(r"[a-z][a-z0-9_]*", f.slug), state, context, "slug must be lower-case")
        need(0 <= f.x <= 23 and 0 <= f.y <= 20, state, context, "outside the x <= 23 band")
        need(f.cost in (5, 10), state, context, "cost must be 5 or 10")
        need(f.era in ERAS, state, context, "unknown era " + f.era)
        need(all(s in seams.SUBJECTS for s in f.subjects) and len(f.subjects) == 2 and f.subjects[0] != f.subjects[1],
             state, context, "icon needs two different library subjects")
        need(title_fits(f.title), state, context, "title does not fit three caption lines: " + f.title)
        need(len(f.desc.split()) >= 18, state, context, "description is too short")
        for other in rows.get(f.y, []):
            need(abs(other.x - f.x) >= 2, state, context, "caption overlaps " + other.slug)
        rows.setdefault(f.y, []).append(f)
        for group in f.parents:
            for ref in (group if isinstance(group, tuple) else (group,)):
                need(ref in by, state, context, "unknown prerequisite " + ref)
                need(by[ref].y < f.y, state, context, "prerequisite %s is not above it" % ref)
        for ref in f.excludes:
            need(ref in by and ref != f.slug, state, context, "unknown exclusion " + ref)
        if f.event:
            need(f.event in events, state, context, "unknown event " + f.event)
        if f.regime:
            need(f.regime in {r.slug for r in state.REGIMES}, state, context, "unknown regime " + f.regime)
        if f.regime or reaches_regime(f.reward):
            need(f.ai == 0, state, context, "a focus that reaches a regime effect needs ai_will_do factor 0")
        expand(state, f.reward, context, ideas, events)
    regimes_used = {f.regime for f in state.FOCUSES if f.regime} | {t[7:] for f in state.FOCUSES for t in f.reward if t.startswith("regime:")}
    need(regimes_used == {r.slug for r in state.REGIMES}, state, "regimes", "every political path needs a focus")
    turns = {f.event for f in state.FOCUSES if f.event and (f.regime or reaches_regime(f.reward))}
    for e in state.EVENTS:
        key = events[e.slug]
        text = seams.event_text(e.paragraphs, e.layer, e.citation)
        problems = seams.event_problems(text)
        need(not problems, state, key, "event text: " + ", ".join(problems))
        words = len(text.rsplit("\n\n", 1)[0].split())
        need(words >= (260 if e.slug in turns else 200), state, key,
             "%d words; political turns need 260 and other events 200" % words)
        need("—" not in text and "–" not in text, state, key, "use plain hyphens, not dashes")
        need(len(text) <= 3000, state, key, "event body longer than 3000 characters (event-style PNG bound)")
        need(title20(e.title) <= 400, state, key, "event title wider than one ACBriefing20 line: " + e.title)
        need(e.picture in EVENT_PICTURES, state, key, "unknown event picture " + e.picture)
        need(1 <= len(e.options) <= 3, state, key, "one to three options")
        for n, option in enumerate(e.options):
            if reaches_regime(option.effects):
                need(option.ai == 0, state, key, "an option that reaches a regime effect needs ai_chance 0")
            expand(state, option.effects, key, ideas, events)
            need(title20(option.name) <= 1500, state, key, "option text too long")
    fired = {f.event for f in state.FOCUSES if f.event} | {t[6:] for f in state.FOCUSES for t in f.reward if t.startswith("event:")}
    fired |= {t[6:] for e in state.EVENTS for o in e.options for t in o.effects if t.startswith("event:")}
    fired |= {t[6:] for d in state.DECISIONS for t in d.effects if t.startswith("event:")}
    need(fired == set(events), state, "events", "events never fired: " + ", ".join(sorted(set(events) - fired)))
    for i in state.IDEAS:
        need(set(i.modifiers) <= MODIFIERS, state, idea_id(state, i.slug), "unreviewed modifier " + ", ".join(sorted(set(i.modifiers) - MODIFIERS)))
        need(all(s in seams.SUBJECTS for s in i.subjects), state, idea_id(state, i.slug), "unknown subject")
    for r in state.REGIMES:
        need(r.party in IDEOLOGIES and set(r.popularities) == IDEOLOGIES and sum(r.popularities.values()) == 100,
             state, r.slug, "popularities must cover every ideology and sum to 100")
        need(r.popularities[r.party] == max(r.popularities.values()), state, r.slug, "the ruling party should lead the seeded popularity")
    for d in state.DECISIONS:
        need(not reaches_regime(d.effects), state, d.slug, "decisions never change governments")
        expand(state, d.effects, decision_id(state, d.slug), ideas, events)
    for name in state.FLAGS:
        need(re.fullmatch(r"[a-z][a-z0-9_]*", name), state, name, "flag names are lower-case")
        need(name not in by, state, name, "flag name repeats a focus slug")
    if PROBLEMS:
        found = list(PROBLEMS)
        PROBLEMS.clear()
        raise Problem("\n  ".join(["%d problems:" % len(found)] + found))
    return len(state.FOCUSES), len(state.EVENTS)


# --- generation --------------------------------------------------------------

def focus_tree(state):
    tag = state.TAG
    ideas = {i.slug for i in state.IDEAS}
    events = event_ids(state)
    excludes = {f.slug: set(f.excludes) for f in state.FOCUSES}
    for f in state.FOCUSES:
        for ref in f.excludes:
            excludes[ref].add(f.slug)
    max_x = max(f.x for f in state.FOCUSES)
    root = state.FOCUSES[0]
    body = "id = %s\n" % tree_id(tag)
    body += "country = { factor = 0 modifier = { add = 45 tag = %s original_tag = %s } }\n" % (tag, tag)
    body += "default = no\nreset_on_civilwar = no\n"
    body += "continuous_focus_position = { x = %d y = 16 }\n" % ((max_x + 4) * 96)
    body += "initial_show_position = { focus = %s }\n" % fid(state, root.slug)
    for f in state.FOCUSES:
        ident = fid(state, f.slug)
        loc(ident, f.title)
        loc(ident + "_desc", f.desc + "\\n\\n" + focus_layer(f))
        text = "id = %s\nicon = GFX_ac_ud_focus_%s\nx = %d\ny = %d\ncost = %d\n" % (ident, ident, f.x, f.y, f.cost)
        for group in f.parents:
            refs = group if isinstance(group, tuple) else (group,)
            text += block("prerequisite", " ".join("focus = " + fid(state, r) for r in refs))
        if excludes[f.slug]:
            text += block("mutually_exclusive", " ".join("focus = " + fid(state, r) for r in sorted(excludes[f.slug])))
        conditions = [c for c in ("original_tag = " + tag, ERAS[f.era], f.available) if c]
        text += block("available", "\n".join(conditions))
        if f.bypass:
            text += block("bypass", f.bypass)
        text += block("ai_will_do", "factor = %d" % (0 if (f.regime or reaches_regime(f.reward)) else f.ai))
        reward = list(f.reward)
        if f.regime:
            reward.append("regime:" + f.regime)
        if f.event:
            reward.append("event:" + f.event)
        effects = expand(state, reward, ident, ideas, events)
        text += block("completion_reward", effects if effects else "add_stability = 0.01")
        body += block("focus", text)
    loc(tree_id(tag), state.TREE_TITLE)
    loc(tree_id(tag) + "_desc", state.TREE_DESC + "\\n\\nProvisional gameplay. Geography, resources and neighbours are mod provenance.")
    return HEADER + block("focus_tree", body)


def focus_layer(f):
    note = {
        "open": "Provisional gameplay. Geography, resources and neighbours are mod provenance.",
        "ulysses": "Provisional gameplay, opened by the official Ulysses announcement (ACES Chronicle, 1996 / 04.20).",
        "coup": "Provisional gameplay, opened by the official Usea-wide coup (ACES Chronicle, 1997 / 05.30).",
        "stonehenge": "Provisional gameplay, opened by the official completion of Stonehenge (ACES Chronicle, 1998 / 06.19).",
        "impact": "Provisional gameplay, opened by the official impact (ACES Chronicle, 1999 / 07.08).",
        "closure": "Provisional gameplay, opened by the official Erusean refugee closure (ACES Chronicle, 2000 / 04.21).",
        "late": "Provisional gameplay for the 2003-2005 war years (ACES Chronicle, 2003 / SUMMER onward).",
        "war": "Provisional gameplay. The war it answers is official (ACES Chronicle, 2003 / SUMMER onward).",
        "isaf": "Provisional gameplay. ISAF's founding is official (ACES Chronicle, 2003 / 08.22).",
        "averted": "Provisional gameplay on the averted-war alternative; in the official chronology the war happens.",
        "postwar": "Provisional gameplay after the Continental War outcome (ACES Chronicle, 2005 / 09.19 for the official ending).",
    }[f.era]
    return note


def build_state_parts(state, parts):
    tag = state.TAG
    ideas = {i.slug for i in state.IDEAS}
    events = event_ids(state)
    OUT["common/national_focus/ac_ud_minor_%s.txt" % tag.lower()] = focus_tree(state)
    for i in state.IDEAS:
        ident = idea_id(state, i.slug)
        loc(ident, i.title)
        loc(ident + "_desc", i.desc + "\\n\\nProvisional gameplay.")
        modifier = "\n".join("%s = %s" % (k, fmt(v)) for k, v in i.modifiers.items())
        parts["ideas"].append(block(ident, "picture = %s\nallowed = { always = no }\nallowed_civil_war = { always = yes }\nremoval_cost = -1\n" % ident +
                                    block("modifier", modifier)))
    for r in state.REGIMES:
        office = office_id(state, r)
        _, body = seams.office_character(tag, r.slug, r.ideology, "GFX_ac_ud_minb_office_%s_%s" % (tag, r.slug))
        parts["characters"].append(body)
        loc(office, r.office)
        loc(office + "_desc", r.office_desc + " An unnamed office government; no individual officeholder is asserted. Provisional gameplay.")
        name, effect = seams.regime_effect(PKG, "%s_%s" % (tag.lower(), r.slug), r.party, office, r.ideology, r.elections, r.popularities)
        assert name == regime_name(state, r.slug)
        parts["effects"].append(effect.replace("\n\t", "\n\t").rstrip("\n") + "\n")
    for e in state.EVENTS:
        key = events[e.slug]
        loc(key + ".t", e.title)
        loc(key + ".d", seams.event_text(e.paragraphs, e.layer, e.citation).replace("\n", "\\n"))
        body = "id = %s\ntitle = %s.t\ndesc = %s.d\npicture = GFX_ac_camp_event_%s\nis_triggered_only = yes\n" % (key, key, key, e.picture)
        body += block("trigger", "original_tag = " + tag)
        for n, option in enumerate(e.options):
            name = "%s.%s" % (key, "abc"[n])
            loc(name, option.name)
            text = "name = %s\n" % name
            if option.trigger:
                text += block("trigger", option.trigger)
            text += block("ai_chance", "factor = %d" % (0 if reaches_regime(option.effects) else option.ai))
            effects = expand(state, option.effects, key, ideas, events)
            if effects:
                text += effects + "\n"
            body += block("option", text)
        parts["events"].append(block("country_event", body))
    adopt = tag + "_ud_adopt_programme"
    loc(adopt, "Adopt the %s" % state.TREE_TITLE)
    loc(adopt + "_desc", "Replace the shared regional or generic programme with %s's national programme once its current focus is idle. Completed focuses are kept. No equipment, factories or historical rewards are granted. Provisional gameplay." % state.NAME)
    guard = "ac_pol_previous_tree_idle = yes NOT = { has_focus_tree = %s }" % tree_id(tag)
    parts["decisions"].append(block(adopt, "icon = ac_ud_minb_%s\nallowed = { original_tag = %s }\n" % (tag.lower(), tag) +
        block("visible", "tag = %s original_tag = %s NOT = { has_focus_tree = %s }" % (tag, tag, tree_id(tag))) +
        block("available", guard) + "cost = 0\nfire_only_once = no\n" +
        block("complete_effect", block("if", block("limit", guard) + "load_focus_tree = { tree = %s keep_completed = yes }" % tree_id(tag))) +
        block("ai_will_do", "base = 10")))
    for d in state.DECISIONS:
        ident = decision_id(state, d.slug)
        loc(ident, d.title)
        loc(ident + "_desc", d.desc + " Costs %d political power and 2 institutional capacity; when the fiscal model is ready, it also books a programme payment. Provisional gameplay." % d.pp)
        available = "political_power >= %d check_variable = { ac_pol_capacity >= 2 } %s NOT = { has_country_flag = ac_ud_minb_programme_cooldown }" % (d.pp, d.requires)
        effects = expand(state, d.effects, ident, ideas, events)
        complete = "add_political_power = -%d\nac_ud_minors_b_pay_programme = yes\n%s\nset_country_flag = { flag = ac_ud_minb_programme_cooldown days = %d }" % (d.pp, effects, d.days_re_enable)
        parts["decisions"].append(block(ident, "icon = ac_ud_minb_%s\nallowed = { original_tag = %s }\n" % (tag.lower(), tag) +
            block("visible", "original_tag = %s %s" % (tag, d.requires)) + block("available", available) +
            "cost = 0\nfire_only_once = no\ndays_re_enable = %d\n" % d.days_re_enable + block("complete_effect", complete) +
            block("ai_will_do", "base = 2")))
    for name, label in state.FLAGS.items():
        loc(fid(state, name), label)


def build(states):
    OUT.clear()
    LOC.clear()
    parts = {"ideas": [], "effects": [], "characters": [], "events": [], "decisions": []}
    for state in states:
        build_state_parts(state, parts)
    tags = [s.TAG for s in states]
    member = block("ac_ud_minors_b_member", block("OR", "\n".join("original_tag = " + t for t in tags)))
    OUT["common/scripted_triggers/ac_ud_minors_b.txt"] = HEADER + member
    pay = block("ac_ud_minors_b_pay_programme",
                "set_temp_variable = { ac_pol_capacity_delta = -2 }\nac_pol_change_capacity = yes\n" +
                block("if", block("limit", "ac_econ_ready = yes") + "ac_econ_pay_programme = yes"))
    OUT["common/scripted_effects/ac_ud_minors_b.txt"] = HEADER + pay + "\n" + "\n".join(parts["effects"])
    OUT["common/ideas/ac_ud_minors_b.txt"] = HEADER + block("ideas", block("country", "\n".join(parts["ideas"])))
    OUT["common/characters/ac_ud_minors_b.txt"] = HEADER + "characters = {\n" + "".join(parts["characters"]) + "}\n"
    OUT["events/ac_ud_minors_b.txt"] = HEADER + "add_namespace = %s\n\n" % NS + "\n".join(parts["events"])
    OUT["common/decisions/ac_ud_minors_b.txt"] = HEADER + block("ac_ud_minors_b_programmes", "\n".join(parts["decisions"]))
    OUT["common/decisions/categories/ac_ud_minors_b.txt"] = HEADER + block(
        "ac_ud_minors_b_programmes", "icon = ac_ud_minors_b\nallowed = { ac_ud_minors_b_member = yes }\nvisible = { ac_ud_minors_b_member = yes }\nvisible_when_empty = no\npriority = 60")
    loc("ac_ud_minors_b_programmes", "National Programmes")
    loc("ac_ud_minors_b_programmes_desc", "National programmes of the smaller Usean states. Each one is paid in political power and institutional capacity, and through the fiscal model when it is ready. Provisional gameplay.")
    loc("ac_ud_minb_programme_cooldown", "A national programme was started within its cooldown")
    OUT["localisation/english/ac_ud_minors_b_l_english.yml"] = "\ufeffl_english:\n" + "".join(
        ' %s:0 "%s"\n' % (k, v) for k, v in sorted(LOC.items()))
    counts = {s.TAG: len(s.FOCUSES) for s in states}
    budget = {"package": PKG, "marker": None, "focuses": counts,
              "trees": {tree_id(s.TAG): len(s.FOCUSES) for s in states}, "events": sum(len(s.EVENTS) for s in states)}
    OUT["../../tools/usea_depth/minors_b/budget.json"] = json.dumps(budget, indent=1) + "\n"
    OUT["../../docs/usea_depth/MINORS_B.md"] = ledger(states)
    return OUT


def ledger(states):
    from ledger import render
    return render(states, event_ids, regime_name, office_id, tree_id, fid)


def all_states():
    return [load_state(tag) for tag in ORDER if (HERE / "states" / (tag.lower() + ".py")).exists()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--validate", metavar="TAG")
    args = parser.parse_args()
    try:
        if args.validate:
            state = load_state(args.validate.upper())
            focuses, events = validate(state)
            LOC.clear()
            build_state_parts(state, {"ideas": [], "effects": [], "characters": [], "events": [], "decisions": []})
            print("%s: %d focuses, %d events, %d ideas, %d political paths: valid" % (state.TAG, focuses, events, len(state.IDEAS), len(state.REGIMES)))
            return
        states = all_states()
        for state in states:
            validate(state)
        outputs = build(states)
    except Problem as error:
        raise SystemExit("Minors B: " + str(error))
    differs = []
    for relative, text in outputs.items():
        path = (MOD / relative).resolve()
        data = text.encode("utf-8")
        if args.check:
            if not path.exists() or path.read_bytes().replace(b"\r\n", b"\n") != data:
                differs.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    if differs:
        raise SystemExit("Minors B output differs: " + ", ".join(differs))
    print("Minors B: %d states, %d focuses, %d events, %d outputs %s" % (
        len(states), sum(len(s.FOCUSES) for s in states), sum(len(s.EVENTS) for s in states), len(outputs),
        "verified" if args.check else "generated"))


if __name__ == "__main__":
    main()
