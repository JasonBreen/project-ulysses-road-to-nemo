"""Compile persistent Usean partner programmes. --check never writes.

Package 1 owns political capacity and fiscal payment; ac_ucw owns the calendar,
war, faction, project and settlement state. This bundle only consumes those
contracts. No focus creates factories, equipment, borders or a new war.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

from content import COUNTRIES, FOCUSES, PHASES, POLICY_MODIFIERS
from scopes import SCOPES, CAPABILITIES

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / "mod/2985041246"
OUT = {}; LOC = {}; EVENTS = []
NOTE = "# Authored gameplay; source: tools/usean_partners/content.py and build.py.\n"
# Separate authoring modules share this compiler state in CLI and test imports.
sys.modules.setdefault("usean_partner_builder", sys.modules[__name__])


def block(key, body):
    return key + " = {\n" + "\n".join("\t" + line if line else "" for line in body.splitlines()) + "\n}\n"


def guard(condition, body):
    return block("if", "limit = { " + condition + " }\n" + body)


def loc(key, text):
    if key in LOC:
        raise ValueError("Duplicate localization: " + key)
    LOC[key] = text
    return key


def emit(relative, text):
    OUT[relative] = NOTE + text


def row_at(tag, phase, row, lane):
    return next(f for f in FOCUSES if (f.tag, f.phase, f.row, f.lane) == (tag, phase, row, lane))


# Earned capabilities name their actual authored focus, so the decision systems
# grow out of national content rather than appearing fully formed in January.
LEASE_UNLOCKS = {
    "SNS": {"network": "district_switchboards", "protection": "protection_inventory"},
    "AMB": {"reserve": "service_inventory", "transport": "transport_returns"},
    "UGE": {"dispersal": "depot_register", "mobility": "mobility_return", "receiving": "receiving_contacts", "reserve": "reserve_space"},
    "DEL": {"inspection": "inspection_office", "command": "requisition_register"},
}
OFFER_UNLOCKS = {"SNS": "coalition_contact", "AMB": "coalition_capacity", "UGE": "coalition_mobility", "DEL": "coalition_commitment"}


def earned(tag, suffix):
    return "has_country_flag = " + tag + "_up_" + suffix + "_done"


def reward_tooltip(row):
    cfg = COUNTRIES[row.tag]
    text = cfg["axis_titles"][row.lane] + ": +4 (maximum 100). The national programme's standing benefit and civilian allocation update together."
    if row.phase == "preparedness":
        text += " Work completed before 8 July 1999 also records one preparation credit; later domestic work grants no retrospective preparation."
    if policy_other(row):
        text += " Adopt the enduring policy shown below, including its continuing cost."
    if row.row == cfg["rows"] - 1:
        text += " Advance this service's completed milestone to " + str(PHASES.index(row.phase) + 1) + "/4."
        if row.tag == "AMB" and row.lane == 1:
            text += " Raise the funded spare-slot ceiling by one (maximum six); new slots still require funded service."
        if row.tag == "UGE" and row.lane == 2 and row.phase in ("preparedness", "settlement"):
            text += " Raise the simultaneous service-slot limit by one (maximum four)."
    for kind, suffix in LEASE_UNLOCKS[row.tag].items():
        if row.suffix == suffix:
            title = next(title for item, title, *_ in LEASES[row.tag] if item == kind)
            text += " Unlock funded programme: " + title + "."
    if row.suffix == OFFER_UNLOCKS[row.tag]:
        text += " Unlock the once-only bounded FCU service offer; acceptance remains conditional and is never a focus prerequisite."
    if row.row == 2 and row.lane == 0:
        text += " Programme authorisations now consume one institutional capacity instead of two."
    if row.id in CAPABILITIES:
        scope = CAPABILITIES[row.id]
        text += " Earn the named capability required for '" + scope.title + "'. Its other listed capabilities and a paid national allocation remain necessary; this is not an interchangeable index requirement."
    return text


def availability(row):
    text = "ac_up_active = yes tag = " + row.tag
    if row.phase == "preparedness" and row.lane == 2:
        text += " date > 1996.4.19 date < 1999.7.8"
    if row.phase == "response" and row.lane == 2:
        text += " date > 1999.7.7"
    if row.phase == "settlement":
        text += " ac_up_settlement_ready = yes"
        if row.row == COUNTRIES[row.tag]["rows"] - 1:
            if row.lane == 0:
                text += " is_subject = no"
            elif row.lane == 1:
                text += " OR = { is_subject = yes has_country_flag = ac_up_was_displaced has_global_flag = ac_ucw_outcome_erusean_victory }"
    return text


def prerequisites(row):
    tag, phase, index, lane = row.tag, row.phase, row.row, row.lane
    last = COUNTRIES[tag]["rows"] - 1
    if phase == "settlement" and index == last and lane == 2:
        return [row_at(tag, phase, last, n).id for n in (0, 1)]
    if index == 0:
        p = PHASES.index(phase)
        return [] if p == 0 else [row_at(tag, PHASES[p - 1], last, lane).id]
    if index == 2 and lane in (0, 1):
        return [row_at(tag, phase, 1, n).id for n in (0, 1)]
    return [row_at(tag, phase, index - 1, lane).id]


def policy_other(row):
    if row.row == 1 and row.lane in (0, 1):
        return row_at(row.tag, row.phase, 1, 1 - row.lane)
    return None


def event_ready(row):
    last = COUNTRIES[row.tag]["rows"] - 1
    if (row.phase, row.row, row.lane) == ("administration", 0, 0):
        return 1
    if (row.phase, row.row, row.lane) == ("administration", last, 0):
        return 2
    if (row.phase, row.row, row.lane) == ("preparedness", 0, 2):
        return 3
    if (row.phase, row.row, row.lane) == ("response", 2, 1):
        return 4
    if (row.phase, row.row, row.lane) == ("settlement", 0, 0):
        return 5
    if (row.phase, row.row, row.lane) == ("settlement", last, 2):
        return 6
    return None


def build_trees(effects):
    for tag, cfg in COUNTRIES.items():
        tree = "ac_up_" + tag.lower() + "_tree"
        loc(tree, cfg["name"] + ": " + cfg["category"])
        loc(tree + "_desc", "National capacity, enduring choices and practical services through the Usean crisis. The national programme branches are authored gameplay alternatives.")
        panel_x = (max(r.x for r in FOCUSES if r.tag == tag) + 4) * 96
        body = f"id = {tree}\ncountry = {{ factor = 0 modifier = {{ add = 40 tag = {tag} original_tag = {tag} }} }}\ndefault = no\ncontinuous_focus_position = {{ x = {panel_x} y = 16 }}\n"
        for row in (r for r in FOCUSES if r.tag == tag):
            loc(row.id, row.title); loc(row.id + "_desc", row.desc)
            loc(row.id + "_done", row.title + " completed")
            node = f"id = {row.id}\nicon = GFX_ac_up_focus_{row.id}\nx = {row.x}\ny = {row.y}\ncost = {row.cost}\n"
            required = prerequisites(row)
            if required:
                node += block("prerequisite", " ".join("focus = " + r for r in required))
            other = policy_other(row)
            if other:
                node += block("mutually_exclusive", "focus = " + other.id)
            if row.phase == "settlement" and row.row == cfg["rows"] - 1 and row.lane in (0, 1):
                node += block("mutually_exclusive", "focus = " + row_at(tag, row.phase, row.row, 1 - row.lane).id)
            node += block("available", availability(row))
            if row.phase == "preparedness" and row.lane == 2:
                node += block("bypass", "date > 1999.7.7")
            if other and row.lane == 1:
                node += block("ai_will_do", "factor = 40")
            else:
                node += block("ai_will_do", "factor = 60")
            node += "cancel_if_invalid = yes\ncontinue_if_invalid = no\n"
            loc(row.id + "_tt", reward_tooltip(row))
            tooltip = "custom_effect_tooltip = " + row.id + "_tt\n"
            if other:
                tooltip += block("effect_tooltip", "add_ideas = " + row.id + "_spirit")
            node += block("completion_reward", tooltip + block("hidden_effect", row.id + "_reward = yes"))
            node += "search_filters = { FOCUS_FILTER_POLITICAL FOCUS_FILTER_INDUSTRY }\n"
            body += block("focus", node)
            axis = cfg["axes"][row.lane]
            reward = f"set_country_flag = {row.id}_done\nadd_to_variable = {{ ac_up_{tag.lower()}_{axis} = 4 }}\n"
            if row.phase == "preparedness":
                reward += guard("date < 1999.7.8", "add_to_variable = { ac_up_preparedness = 1 }")
            if other:
                reward += f"remove_ideas = {other.id}_spirit\nadd_ideas = {row.id}_spirit\n"
            if row.row == cfg["rows"] - 1:
                reward += f"set_variable = {{ ac_up_{tag.lower()}_{axis}_level = {PHASES.index(row.phase) + 1} }}\n"
            if row.row == 2 and row.lane == 0:
                reward += "set_country_flag = ac_up_efficient_authorisations\n"
            ready = event_ready(row)
            if ready:
                reward += f"set_country_flag = ac_up_event_{ready}_ready\n"
            reward += "ac_up_bound = yes\nac_up_recalculate = yes"
            condition = availability(row) + " NOT = { has_country_flag = " + row.id + "_done }"
            if other:
                condition += " NOT = { has_country_flag = " + other.id + "_done }"
            effects[row.id + "_reward"] = guard(condition, reward)
        emit("common/national_focus/" + tag + ".txt", block("focus_tree", body))


def build_core(triggers, effects):
    for key, title in {
        "ac_up_preparedness": "Verified preparation", "ac_up_amber_slots": "Funded spare service slots",
        "ac_up_amber_limit": "Funded spare-slot ceiling", "ac_up_uge_used": "Occupied service slots",
        "ac_up_uge_limit": "Simultaneous service-slot limit", "ac_up_del_cases": "Verified inspection cases",
        "ac_up_del_obligations": "Unresolved command obligations",
        "ac_up_sns_contact_records": "Verified continuity records",
        "ac_up_sns_protection_records": "Verified protection records",
    }.items():
        loc(key, title)
    loc("ac_up_cost_tt", "Costs 25 political power and 2 institutional capacity (1 after authorisation reform). The fiscal programme charge also applies whenever that system is ready. The action rechecks payment before granting a service.")
    loc("ac_up_allocation_lock", "The current service allocation interval remains in progress")
    loc("ac_up_review_cooldown", "A recently funded national review still reserves its allocation")
    loc("ac_up_efficient_authorisations", "Programme authorisation reforms completed")
    participant = "OR = { " + " ".join(f"AND = {{ tag = {tag} original_tag = {tag} }}" for tag in COUNTRIES) + " }"
    triggers["ac_up_participant"] = participant
    triggers["ac_up_active"] = "ac_up_participant = yes has_country_flag = ac_up_initialized has_capitulated = no"
    triggers["ac_up_settlement_ready"] = "ac_up_active = yes OR = { ac_ucw_war_over = yes has_global_flag = ac_ucw_war_averted AND = { date > 2005.12.30 has_war = no NOT = { has_global_flag = ac_ucw_war_started } } }"
    triggers["ac_up_can_fund"] = "ac_up_active = yes political_power >= 25 ac_pol_active = yes OR = { AND = { has_country_flag = ac_up_efficient_authorisations check_variable = { ac_pol_capacity > 0 } } check_variable = { ac_pol_capacity > 1 } } OR = { ac_econ_ready = no ac_econ_can_pay_programme = yes }"
    effects["ac_up_pay_programme"] = guard("ac_up_can_fund = yes", "add_political_power = -25\nset_temp_variable = { ac_pol_capacity_delta = -2 }\n" + guard("has_country_flag = ac_up_efficient_authorisations", "set_temp_variable = { ac_pol_capacity_delta = -1 }") + "ac_pol_change_capacity = yes\n" + guard("ac_econ_ready = yes", "ac_econ_pay_programme = yes"))
    bound = "clamp_variable = { var = ac_up_preparedness min = 0 max = 20 }\n"
    initialize = "set_country_flag = ac_up_initialized\n" + guard("NOT = { has_variable = ac_up_preparedness }", "set_variable = { ac_up_preparedness = 0 }")
    for tag, cfg in COUNTRIES.items():
        fields = ["ac_up_" + tag.lower() + "_" + axis for axis in cfg["axes"]]
        for name, title in zip(fields, cfg["axis_titles"]):
            loc(name, title); loc(name + "_level", title + ": completed milestone")
        initialize += guard("tag = " + tag, "".join(guard("NOT = { has_variable = " + name + " }", f"set_variable = {{ {name} = 0 }}") + guard("NOT = { has_variable = " + name + "_level }", f"set_variable = {{ {name}_level = 0 }}") for name in fields))
        bound += guard("tag = " + tag, "\n".join(f"clamp_variable = {{ var = {name} min = 0 max = 100 }}\nclamp_variable = {{ var = {name}_level min = 0 max = 4 }}" for name in fields))
    for name, maximum in [("ac_up_amber_slots", 6), ("ac_up_uge_used", 4), ("ac_up_del_cases", 6), ("ac_up_del_obligations", 3), ("ac_up_sns_contact_records", 6), ("ac_up_sns_protection_records", 6)]:
        initialize += guard("NOT = { has_variable = " + name + " }", f"set_variable = {{ {name} = 0 }}")
        bound += f"clamp_variable = {{ var = {name} min = 0 max = {maximum} }}\n"
    initialize += guard("date > 1991.1.31", "set_country_flag = ac_up_event_1_past") + block("else", "set_country_flag = ac_up_event_1_ready")
    initialize += guard("date > 1999.7.7", "set_country_flag = ac_up_event_3_past\nset_country_flag = ac_up_late_crisis")
    initialize += "ac_up_bound = yes\nac_up_recalculate = yes"
    effects["ac_up_initialize"] = guard("ac_up_participant = yes NOT = { has_country_flag = ac_up_initialized }", initialize)
    effects["ac_up_bound"] = bound
    recalc = ""
    mods = []
    mapping = {
        "SNS": [("surrender_limit", "continuity", .0005), ("stability_factor", "protection", .0003), ("supply_consumption_factor", "dispatch", -.0004)],
        "AMB": [("industrial_capacity_factory", "development", .00025), ("supply_consumption_factor", "service", -.0003), ("production_speed_buildings_factor", "transport", .00035)],
        "UGE": [("supply_consumption_factor", "dispersal", -.0004), ("army_speed_factor", "mobility", .00035), ("surrender_limit", "reserve", .00025)],
        "DEL": [("stability_factor", "oversight", .0003), ("planning_speed", "command", .0004), ("research_speed_factor", "records", .0002)],
    }
    for tag, cfg in COUNTRIES.items():
        body = ""; modifier = "icon = GFX_idea_ac_up_" + tag.lower() + "_programme\nenable = { ac_up_active = yes tag = " + tag + " }\n"
        for key, axis, multiplier in mapping[tag]:
            name = "ac_up_bonus_" + key
            body += f"set_variable = {{ {name} = ac_up_{tag.lower()}_{axis} }}\nmultiply_variable = {{ {name} = {multiplier} }}\n"
            modifier += key + " = " + name + "\n"
        body += "set_variable = { ac_up_programme_burden = 0 }\n"
        for axis in cfg["axes"]:
            body += f"add_to_variable = {{ ac_up_programme_burden = ac_up_{tag.lower()}_{axis} }}\n"
        body += "multiply_variable = { ac_up_programme_burden = 0.00015 }\nset_variable = { ac_up_public_record_bonus = 0 }\nset_variable = { ac_up_readiness_record_bonus = 0 }\n"
        body += guard("has_country_flag = ac_up_public_record", "set_variable = { ac_up_public_record_bonus = 0.005 }\nadd_to_variable = { ac_up_programme_burden = 0.003 }")
        body += guard("has_country_flag = ac_up_readiness_record", "set_variable = { ac_up_readiness_record_bonus = 0.01 }\nadd_to_variable = { ac_up_programme_burden = 0.005 }")
        if tag == "DEL":
            body += "set_temp_variable = { ac_up_unclosed_dockets = ac_up_del_obligations }\nmultiply_temp_variable = { ac_up_unclosed_dockets = 0.002 }\nadd_to_variable = { ac_up_programme_burden = ac_up_unclosed_dockets }\n"
        # Add narrative bonuses to an existing modifier rather than defining
        # the same property twice in a dynamic modifier block.
        stability = "ac_up_bonus_stability_factor" if tag in ("SNS", "DEL") else "ac_up_public_record_bonus"
        if tag in ("SNS", "DEL"):
            body += "add_to_variable = { ac_up_bonus_stability_factor = ac_up_public_record_bonus }\n"
        else:
            modifier += "stability_factor = " + stability + "\n"
        modifier += "army_org_factor = ac_up_readiness_record_bonus\n"
        modifier += "consumer_goods_factor = ac_up_programme_burden\n"
        body += guard("NOT = { has_dynamic_modifier = { modifier = ac_up_" + tag.lower() + "_programme } }", "add_dynamic_modifier = { modifier = ac_up_" + tag.lower() + "_programme }")
        if tag == "UGE":
            body += "set_variable = { ac_up_uge_limit = 2 }\n"
            body += guard("check_variable = { ac_up_uge_reserve_level > 1 }", "add_to_variable = { ac_up_uge_limit = 1 }")
            body += guard("check_variable = { ac_up_uge_reserve_level > 3 }", "add_to_variable = { ac_up_uge_limit = 1 }")
        if tag == "AMB":
            body += "set_variable = { ac_up_amber_limit = 2 }\nadd_to_variable = { ac_up_amber_limit = ac_up_amb_service_level }\n"
        recalc += guard("tag = " + tag, body)
        mods.append(block("ac_up_" + tag.lower() + "_programme", modifier))
        loc("ac_up_" + tag.lower() + "_programme", cfg["name"] + ": National Service Programme")
        loc("ac_up_" + tag.lower() + "_programme_desc", "A bounded national service capability, supported by continuing civilian allocations. Capacity indices are provisional gameplay measures.")
    effects["ac_up_recalculate"] = guard("ac_up_active = yes", recalc)
    effects["ac_up_apply_preparation"] = guard("ac_up_active = yes has_country_flag = ac_ucw_started NOT = { has_country_flag = ac_up_preparation_applied }", "set_country_flag = ac_up_preparation_applied\nset_temp_variable = { ac_up_preparation_credit = ac_up_preparedness }\nmultiply_temp_variable = { ac_up_preparation_credit = 0.3 }\nadd_to_variable = { ac_ucw_recovery = ac_up_preparation_credit }\nmultiply_temp_variable = { ac_up_preparation_credit = -1 }\nadd_to_variable = { ac_ucw_pressure = ac_up_preparation_credit }\nac_ucw_bound = yes")
    effects["ac_up_recovery_credit"] = guard("ac_up_active = yes has_country_flag = ac_ucw_started", "add_to_variable = { ac_ucw_recovery = 2 }\nadd_to_variable = { ac_ucw_pressure = -1 }\n" + guard("has_country_flag = ac_up_ordinary_service", "add_to_variable = { ac_ucw_recovery = 1 }") + "ac_ucw_bound = yes")
    emit("common/dynamic_modifiers/ac_usean_partners.txt", "\n".join(mods))


LEASES = {
    "SNS": [("network", "Rehearse the Continuity Network", "communications", "surrender_limit = 0.015\nconsumer_goods_factor = 0.01"), ("protection", "Renew a Protection Service", "shelter", "stability_factor = 0.02\nconsumer_goods_factor = 0.015")],
    "AMB": [("reserve", "Fund a Spare Service Slot", "logistics", "industrial_capacity_factory = -0.01\nconsumer_goods_factor = 0.01"), ("transport", "Authorise a Domestic Transport Service", "rail", "supply_consumption_factor = -0.02\nconsumer_goods_factor = 0.015")],
    "UGE": [("dispersal", "Lease Dispersed Service Capacity", "logistics", "supply_consumption_factor = -0.02\nconsumer_goods_factor = 0.015"), ("mobility", "Lease an Emergency Mobility Slot", "bridge", "army_speed_factor = 0.03\nproduction_speed_buildings_factor = -0.015"), ("receiving", "Lease a Receiving Service Slot", "civil", "stability_factor = 0.02\npolitical_power_factor = -0.02"), ("reserve", "Lease a Readiness Reserve Slot", "command", "army_org_factor = 0.025\nconsumer_goods_factor = 0.015")],
    "DEL": [("inspection", "Authorise an Inspection Rota", "scales", "stability_factor = 0.02\npolitical_power_factor = -0.02"), ("command", "Accept a Bounded Command Obligation", "command", "planning_speed = 0.03\nconsumer_goods_factor = 0.015")],
}


def build_programmes(effects):
    ideas = []; decisions = {}; categories = []; ticks = ""; suspend = "set_country_flag = ac_up_was_displaced\n"
    for tag, cfg in COUNTRIES.items():
        members = []
        category = "ac_up_" + tag.lower() + "_programmes"
        categories.append(block(category, f"icon = ac_up_{tag.lower()}_programmes\nallowed = {{ tag = {tag} original_tag = {tag} }}\nvisible = {{ ac_up_active = yes }}"))
        loc(category, cfg["name"] + ": " + cfg["category"])
        stats = "\n".join(label + ": [?ac_up_" + tag.lower() + "_" + axis + "|0]/100" for label, axis in zip(cfg["axis_titles"], cfg["axes"]))
        extra = {"SNS": "Continuity and protection services renew for 180 days. Stonehenge work observes the existing project's state.", "AMB": "Funded spare slots: [?ac_up_amber_slots|0]/[?ac_up_amber_limit|0]. Completed service milestones raise the funded ceiling from two to six. A domestic transport service or coalition offer spends one slot.", "UGE": "Occupied slots: [?ac_up_uge_used|0]/[?ac_up_uge_limit|0]. Each lease occupies capacity until it expires or is released.", "DEL": "Verified cases: [?ac_up_del_cases|0]/6. Unresolved command obligations: [?ac_up_del_obligations|0]/3. An obligation survives service expiry or displacement until a verified docket closes it. Each unresolved obligation adds a 0.2% consumer-goods factor burden. Three unresolved obligations prevent another command service."}[tag]
        if tag == "SNS":
            extra += " Verified continuity records: [?ac_up_sns_contact_records|0]/6. Verified protection records: [?ac_up_sns_protection_records|0]/6. Completed services earn these records; operational scopes consume them."
        loc(category + "_desc", stats + "\n\n" + extra + "\n\nA funded programme costs 25 political power and 2 institutional capacity, reduced to 1 after authorisation reforms, plus the fiscal programme charge when that system is ready. Operational scopes last 90 days and require specific earned capabilities plus the country's finite service resource. These indices do not create physical equipment.")
        policy_rows = [r for r in FOCUSES if r.tag == tag and policy_other(r)]
        for row in policy_rows:
            ident = row.id + "_spirit"; loc(ident, row.title); loc(ident + "_desc", row.desc)
            modifier = POLICY_MODIFIERS[tag][PHASES.index(row.phase)][row.lane]
            ideas.append(block(ident, f"picture = ac_up_idea_{ident}\nallowed = {{ always = no }}\nallowed_civil_war = {{ always = no }}\nremoval_cost = -1\n" + block("modifier", modifier)))
            suspend += guard("tag = " + tag, "remove_ideas = " + ident)
        country_tick = ""
        for kind, title, subject, modifier in LEASES[tag]:
            ident = f"{tag}_up_{kind}_programme"; active = ident + "_active"; window = ident + "_window"; idea = ident + "_spirit"
            loc(ident, title)
            unlock = LEASE_UNLOCKS[tag][kind]
            unlock_title = next(r.title for r in FOCUSES if r.id == tag + "_up_" + unlock)
            loc(ident + "_desc", "Requires completed national work: " + unlock_title + ". Fund a bounded 180-day service. Its benefits carry the displayed continuing burden. Completion records useful work once; interruption forfeits the cost. A renewed service requires a new allocation.")
            loc(idea, title); loc(idea + "_desc", "A funded, temporary national service with a continuing opportunity cost. The underlying physical forces and supplies remain separate.")
            ideas.append(block(idea, f"picture = ac_up_idea_{idea}\nallowed = {{ always = no }}\nremoval_cost = -1\n" + block("modifier", modifier)))
            condition = "ac_up_can_fund = yes " + earned(tag, unlock) + " NOT = { has_country_flag = " + active + " } NOT = { has_country_flag = ac_up_allocation_lock }"
            if tag == "AMB" and kind == "transport":
                condition += " check_variable = { ac_up_amber_slots > 0 }"
            if tag == "AMB" and kind == "reserve":
                condition += " check_variable = { ac_up_amber_slots < ac_up_amber_limit }"
            if tag == "UGE":
                condition += " check_variable = { ac_up_uge_used < ac_up_uge_limit }"
            if tag == "DEL" and kind == "command":
                condition += " check_variable = { ac_up_del_obligations < 3 }"
            if tag == "DEL" and kind == "inspection":
                condition += " check_variable = { ac_up_del_cases < 6 }"
            payment = "ac_up_pay_programme = yes\nset_country_flag = " + active + "\nset_country_flag = { flag = " + window + " days = 180 }\nset_country_flag = { flag = ac_up_allocation_lock days = " + ("30" if tag == "UGE" else "90") + " }\nadd_ideas = " + idea + "\n"
            if tag == "AMB" and kind == "transport":
                payment += "add_to_variable = { ac_up_amber_slots = -1 }\n"
            if tag == "UGE":
                payment += "add_to_variable = { ac_up_uge_used = 1 }\n"
            if tag == "DEL" and kind == "command":
                payment += "add_to_variable = { ac_up_del_obligations = 1 }\n"
            effects[ident + "_start"] = guard("tag = " + tag + " " + condition, payment + "ac_up_bound = yes")
            complete = f"clr_country_flag = {active}\nclr_country_flag = {window}\nremove_ideas = {idea}\n"
            if tag == "SNS":
                record = "contact" if kind == "network" else "protection"
                complete += f"add_to_variable = {{ ac_up_sns_{record}_records = 1 }}\n"
            if tag == "UGE":
                complete += "add_to_variable = { ac_up_uge_used = -1 }\n"
            if tag == "AMB" and kind == "reserve":
                complete += "add_to_variable = { ac_up_amber_slots = 1 }\n"
            elif tag == "DEL" and kind == "inspection":
                complete += "add_to_variable = { ac_up_del_cases = 1 }\n"
            elif tag == "DEL" and kind == "command":
                complete += "ac_up_recovery_credit = yes\n"
            elif tag == "SNS" and kind == "protection":
                complete += guard("date < 1999.7.8", "add_to_variable = { ac_up_preparedness = 2 }") + block("else", "ac_up_recovery_credit = yes")
            else:
                complete += "ac_up_recovery_credit = yes\n"
            complete += "ac_up_bound = yes\nac_up_recalculate = yes"
            effects[ident + "_finish"] = guard("ac_up_active = yes tag = " + tag + " has_country_flag = " + active + " NOT = { has_country_flag = " + window + " }", complete)
            country_tick += ident + "_finish = yes\n"
            suspend += guard("tag = " + tag, f"clr_country_flag = {active}\nclr_country_flag = {window}\nremove_ideas = {idea}")
            preview = "custom_effect_tooltip = ac_up_cost_tt\n" + block("effect_tooltip", "add_ideas = " + idea)
            members.append(block(ident, f"icon = ac_up_{tag.lower()}_programme\nallowed = {{ tag = {tag} original_tag = {tag} }}\nvisible = {{ ac_up_active = yes }}\navailable = {{ {condition} }}\ncost = 0\n" + block("complete_effect", preview + block("hidden_effect", ident + "_start = yes")) + "ai_will_do = { base = 2 }"))
        tree = "ac_up_" + tag.lower() + "_tree"
        adopt = tag + "_up_adopt_programme"
        loc(adopt, "Adopt the National Programme"); loc(adopt + "_desc", "After the current generic, regional or continuous focus finishes, adopt the persistent national tree while retaining completed content. This grants no starting forces, industry or expired historical preparation.")
        adopt_condition = f"ac_up_active = yes ac_pol_previous_tree_idle = yes OR = {{ has_focus_tree = generic_focus has_focus_tree = ac_regional_foundation }} NOT = {{ has_focus_tree = {tree} }}"
        members.append(block(adopt, f"icon = ac_up_{tag.lower()}_programme\nallowed = {{ tag = {tag} }}\nvisible = {{ ac_up_active = yes NOT = {{ has_focus_tree = {tree} }} }}\navailable = {{ {adopt_condition} }}\ncost = 0\n" + block("complete_effect", guard(adopt_condition, f"load_focus_tree = {{ tree = {tree} keep_completed = yes }}")) + "ai_will_do = { base = 1 }"))
        decisions[category] = members
        effects["ac_up_" + tag.lower() + "_services"] = guard("ac_up_active = yes tag = " + tag, country_tick)
        ticks += "ac_up_" + tag.lower() + "_services = yes\n"
        restore = ""
        for row in policy_rows:
            restore += guard("has_country_flag = " + row.id + "_done NOT = { has_idea = " + row.id + "_spirit }", "add_ideas = " + row.id + "_spirit")
        effects["ac_up_" + tag.lower() + "_restore_policies"] = guard("ac_up_active = yes tag = " + tag, restore)
        ticks += "ac_up_" + tag.lower() + "_restore_policies = yes\n"
    suspend += "set_variable = { ac_up_uge_used = 0 }\nac_up_scope_suspend = yes\nac_up_interrupt_diplomacy = yes"
    effects["ac_up_interrupt_services"] = guard("ac_up_participant = yes has_country_flag = ac_up_initialized", suspend)
    effects["ac_up_suspend"] = guard("ac_up_participant = yes has_country_flag = ac_up_initialized has_capitulated = yes", "ac_up_interrupt_services = yes")
    effects["ac_up_service_tick"] = ticks
    emit("common/ideas/ac_usean_partners.txt", block("ideas", block("country", "\n".join(ideas))))
    emit("common/decisions/categories/ac_usean_partners.txt", "\n".join(categories))
    return decisions


def outputs():
    OUT.clear(); LOC.clear(); EVENTS.clear()
    effects = {}; triggers = {}
    build_core(triggers, effects)
    build_trees(effects)
    decisions = build_programmes(effects)
    # Country-specific review rules, reciprocity and authored narrative are
    # separate authoring tables to keep each national system reviewable.
    from narrative import build_narrative
    from programmes import build_country_rules
    from scope_rules import build_scope_rules
    build_country_rules(effects, triggers, decisions)
    build_scope_rules(effects, triggers, decisions)
    build_narrative(effects, triggers)
    emit("events/ac_usean_partners.txt", "add_namespace = ac_up\n\n" + "\n".join(EVENTS))
    weekly = "ac_up_initialize = yes\nac_up_suspend = yes\n" + guard("ac_up_active = yes", "ac_up_apply_preparation = yes\nac_up_service_tick = yes\nac_up_scope_tick = yes\nac_up_diplomacy_tick = yes\nac_up_narrative_tick = yes\nac_up_bound = yes\nac_up_recalculate = yes")
    effects["ac_up_weekly"] = weekly
    emit("common/scripted_effects/ac_usean_partners.txt", "\n".join(block(k, v) for k, v in effects.items()))
    emit("common/scripted_triggers/ac_usean_partners.txt", "\n".join(block(k, v) for k, v in triggers.items()))
    emit("common/decisions/ac_usean_partners.txt", "\n".join(block(k, "\n".join(v)) for k, v in decisions.items()))
    startup = "\n".join(tag + " = { ac_up_initialize = yes }" for tag in COUNTRIES)
    hooks = block("on_startup", block("effect", startup))
    hooks += "\n".join(block("on_weekly_" + tag, block("effect", "ac_up_weekly = yes")) for tag in COUNTRIES)
    hooks += block("on_weekly_FCU", block("effect", "ac_up_fcu_cleanup = yes"))
    # Engine on_annex: ROOT is the winner; FROM is the annexed country. Clear
    # paid work at the interruption, before a later release can finish it.
    hooks += block("on_annex", block("effect", block("FROM", "ac_up_interrupt_services = yes")))
    emit("common/on_actions/ac_usean_partners.txt", block("on_actions", hooks))
    OUT["localisation/english/ac_usean_partners_l_english.yml"] = "\ufeffl_english:\n" + "\n".join(f' {key}:0 "{value.replace(chr(10), chr(92) + "n").replace(chr(34), chr(39))}"' for key, value in LOC.items()) + "\n"
    return dict(OUT)


def check_dependencies():
    required = {"ac_pol_active", "ac_pol_change_capacity", "ac_pol_previous_tree_idle", "ac_econ_can_pay_programme", "ac_econ_pay_programme"}
    text = "\n".join(p.read_text(encoding="utf-8-sig") for folder in ("common/scripted_effects", "common/scripted_triggers") for p in (MOD / folder).glob("*.txt"))
    missing = [name for name in required if name + " = {" not in text and name + "={" not in text]
    if missing:
        raise SystemExit("Integrate Package 1 owners before release: " + ", ".join(sorted(missing)))


def purpose_inventory():
    """Record real consumers; repeated already-earned flags are not purposes."""
    rows = []; baseline = Counter(); remaining = Counter()
    reviews = {"SNS_up_project_burden_review", "SNS_up_stonehenge_liaison", "SNS_up_protection_accounts", "AMB_up_spare_capacity"}
    for row in FOCUSES:
        purposes = []
        if policy_other(row): purposes.append("Enduring exclusive policy with a continuing opportunity cost")
        if row.row == COUNTRIES[row.tag]["rows"] - 1: purposes.append("Complete the service milestone and open the next act or settlement assessment")
        if event_ready(row) not in (None, 1): purposes.append("Open national choice event " + str(event_ready(row)))
        if row.phase == "administration" and row.row == 2 and row.lane == 0: purposes.append("Reduce future programme authorisation cost")
        if row.suffix in LEASE_UNLOCKS[row.tag].values(): purposes.append("Unlock a funded national service")
        if row.suffix == OFFER_UNLOCKS[row.tag]: purposes.append("Unlock the eligible reciprocal FCU offer")
        if row.id in reviews: purposes.append("Unlock the scoped national burden/capacity review")
        if not purposes: baseline[row.tag] += 1
        if row.id in CAPABILITIES:
            scope = CAPABILITIES[row.id]
            purposes.append("Nonfungible capability required for " + scope.id + ": " + scope.purpose)
        if not purposes: remaining[row.tag] += 1
        rows.append(dict(id=row.id, title=row.title, country=row.tag, phase=row.phase, purposes=purposes,
                         scope_consumer=CAPABILITIES[row.id].id if row.id in CAPABILITIES else None,
                         source_layer="original provisional gameplay"))
    if sum(baseline.values()) != 117 or remaining:
        raise ValueError("Unconsumed focus purpose: " + str(dict(remaining)))
    return dict(schema=1, focuses=len(rows), curated_scopes=len(SCOPES), original_sole_axis_counts=dict(baseline),
                remaining_sole_axis_counts={tag:remaining[tag] for tag in COUNTRIES}, rows=rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true"); parser.add_argument("--require-dependencies", action="store_true")
    args = parser.parse_args()
    if args.require_dependencies:
        check_dependencies()
    failures = []
    for relative, text in outputs().items():
        path = MOD / relative
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                failures.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text, encoding="utf-8", newline="\n")
    manifest = HERE / "purposes.json"
    purpose_text = json.dumps(purpose_inventory(), indent=2) + "\n"
    if args.check:
        if not manifest.exists() or manifest.read_text(encoding="utf-8") != purpose_text:
            failures.append("tools/usean_partners/purposes.json")
    else:
        manifest.write_text(purpose_text, encoding="utf-8", newline="\n")
    if failures:
        raise SystemExit("Usean partner output differs: " + ", ".join(failures))
    print("Usean partners: 228 focuses and four national programme systems; " + ("consistent" if args.check else "generated"))


if __name__ == "__main__":
    main()
