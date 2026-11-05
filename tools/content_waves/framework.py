"""Six-node national branch compiler shared by the 2006-2020 content waves.

Every branch has the same reviewable shape as the reconstruction continuations:
a register, two mutually exclusive enduring policies, an operational step, a
review that needs a genuinely completed funded service and a standing settlement.
Each wave owns its own namespace, flags, variables, decisions and events. All
values are provisional gameplay; no history, border, leader, force grant,
faction, war or project state is written by this compiler.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
import re

SUFFIXES = ("register", "policy_a", "policy_b", "operations", "review", "settlement")
GLYPHS = {
    "air", "assembly", "ballot", "bridge", "carrier", "civil", "command", "communications",
    "diplomacy", "document", "economy", "fishing", "gate", "industry", "logistics", "medal",
    "medical", "meteor", "missile", "navy", "peace", "radar", "rail", "rebuild", "refugees",
    "runway", "satellite", "scales", "science", "shelter", "submarine", "telescope", "tools",
    "training", "security",
}


@dataclass(frozen=True)
class Branch:
    tag: str
    key: str
    entry: tuple          # prerequisite focus IDs for the register (OR); empty for a tree root
    gate: str             # additional availability condition for the register only
    titles: tuple         # six focus titles
    descriptions: tuple   # six focus descriptions
    subjects: tuple       # six (primary, secondary) glyph pairs
    policies: tuple       # two (name, benefit, enduring cost)
    services: tuple       # two (title, objective, institution, modifiers)
    scene: tuple          # (title, prose, (open label, protected label))
    final: tuple          # (title, prose)
    service_effect: str = ""     # extra guarded effect when a service period completes
    settlement_effect: str = ""  # extra effect applied once with the settlement
    policy_effects: tuple = ("", "")  # extra effects applied once with policy A / policy B


@dataclass(frozen=True)
class Wave:
    prefix: str           # scripted namespace, e.g. ac_fe
    infix: str            # focus infix, e.g. fe -> ERU_fe_<branch>_<suffix>
    label: str            # human name used in comments and manifests
    source: str           # generator directory under tools/
    countries: dict       # tag -> display name
    eligible: str         # extra country eligibility condition (may be empty)
    branches: tuple
    layout: dict          # branch key -> (root x, root y)
    openings: dict        # tag -> (title, prose, (open label, protected label))
    finals: dict          # tag -> (title, prose, readiness benefit)
    final_ready: dict     # tag -> trigger for the national conclusion
    themes: dict          # tag -> (primary, secondary) glyphs for national art
    weekly_extra: dict = field(default_factory=dict)  # tag -> extra weekly effect
    event_base: int = 10         # first narrative event number; owners use the numbers below it
    extra_tags: tuple = ()       # tags an owner-only wave writes flags for without any branch


def branch_id(branch):
    return f"{branch.tag}_{branch.key}"


def focus_id(wave, branch, index):
    return f"{branch.tag}_{wave.infix}_{branch.key}_{SUFFIXES[index]}"


def service_id(wave, branch, n):
    return f"{branch.tag}_{wave.infix}_{branch.key}_service_{n + 1}"


def block(key, body):
    return key + " = {\n" + "\n".join("\t" + line if line else "" for line in body.splitlines()) + "\n}\n"


def guard(condition, body):
    return block("if", block("limit", condition) + body)


def number(value):
    text = format(value, ".3f").rstrip("0").rstrip(".")
    return "0" if text in ("-0", "") else text


def modifiers(values):
    return "\n".join(key + " = " + number(value) for key, value in values.items())


def improve(benefits, costs):
    return {**{key: round(value * 1.2, 3) for key, value in benefits.items()}, **costs}


def validate(wave):
    seen = set()
    for branch in wave.branches:
        assert branch.tag in wave.countries, branch
        assert len(branch.titles) == len(branch.descriptions) == len(branch.subjects) == 6, branch.key
        assert len(branch.policies) == 2 and len(branch.services) == 2, branch.key
        for pair in branch.subjects:
            unknown = set(pair) - GLYPHS
            assert not unknown, (branch.key, unknown)
        for index in range(6):
            ident = focus_id(wave, branch, index)
            assert ident not in seen, ident
            seen.add(ident)
        for name, benefit, cost in branch.policies:
            assert benefit and cost and not set(benefit) & set(cost), (branch.key, name)
        assert branch_id(branch) in wave.layout, branch.key
    for tag in wave.countries:
        assert tag in wave.openings and tag in wave.finals and tag in wave.final_ready and tag in wave.themes, tag


def positions(wave):
    result = {}
    for branch in wave.branches:
        x, y = wave.layout[branch_id(branch)]
        for index in range(6):
            dx = -2 if index == 1 else 2 if index == 2 else 0
            dy = 0 if index == 0 else 1 if index in (1, 2) else index - 1
            result[focus_id(wave, branch, index)] = (x + dx, y + dy)
    return result


def empty_wave(wave):
    """Fragments for an owner-only wave: no branches, services, trees or narrative.

    Conflict owners whose countries' focus budgets are already complete (the
    Circum-Pacific War) supply every effect, trigger, event, idea, decision and
    on_action hook themselves; the build merges them exactly as it merges an
    owner into a branch wave.
    """
    validate(wave)
    assert not wave.branches and not wave.countries, wave.label
    return dict(loc={}, effects={}, triggers={}, ideas=[], focuses=[], categories=[], decisions=defaultdict(list),
                custom=[], events=[], hooks={}, services=[], positions={})


def compile_wave(wave, event_base=None):
    """Return script/localization fragments for one wave.

    The caller writes the fragments to files, so the build can merge an owner
    module (for example a conflict owner) into the same namespace.
    """
    validate(wave)
    event_base = wave.event_base if event_base is None else event_base
    P = wave.prefix
    loc = {}
    effects = {}
    triggers = {}
    ideas = []
    focuses = []
    categories = []
    decisions = defaultdict(list)
    custom = []
    events = []
    services = [(b, n, service_id(wave, b, n)) for b in wave.branches for n in range(2)]
    where = positions(wave)

    def text(key, value):
        if key in loc:
            raise ValueError(f"Duplicate {wave.label} localization: {key}")
        loc[key] = value

    def idea(ident, title, description, values):
        text(ident, title)
        text(ident + "_desc", description)
        ideas.append(block(ident, "picture = " + ident + "\nallowed = { always = no }\nallowed_civil_war = { always = no }\nremoval_cost = -1\n" + block("modifier", modifiers(values))))

    def decision(ident, tag, title, description, visible, available, action, cost=True, ai=3):
        text(ident, title)
        text(ident + "_desc", description)
        body = f"icon = {P}_{ident}\nallowed = {{ tag = {tag} original_tag = {tag} }}\nvisible = {{ {visible} }}\navailable = {{ {available} }}\ncost = 0\n"
        if cost:
            body += f"custom_cost_trigger = {{ {P}_can_fund = yes }}\ncustom_cost_text = {P}_funded_cost\n"
        body += block("complete_effect", action) + f"ai_will_do = {{ base = {ai if cost else 0} }}\n"
        decisions[f"{P}_{tag.lower()}_services"].append(block(ident, body))

    # Shared runtime ------------------------------------------------------
    triggers[P + "_participant"] = "OR = { " + " ".join(f"AND = {{ tag = {t} original_tag = {t} }}" for t in wave.countries) + " }"
    triggers[P + "_eligible"] = f"{P}_participant = yes any_owned_state = {{ always = yes }} has_capitulated = no {wave.eligible}".strip()
    triggers[P + "_active"] = f"{P}_eligible = yes has_country_flag = {P}_initialized"
    triggers[P + "_idle"] = f"NOT = {{ has_country_flag = {P}_service_active }} check_variable = {{ {P}_current_service = 0 }} NOT = {{ has_country_flag = {P}_service_cooldown }}"
    triggers[P + "_can_fund"] = (f"{P}_active = yes has_war = no {P}_idle = yes political_power >= 35 ac_pol_active = yes "
                                  "check_variable = { ac_pol_capacity >= 4 } OR = { ac_econ_enabled = no ac_econ_can_pay_programme = yes }")
    init = ""
    for variable in (P + "_current_service", P + "_elapsed", P + "_completed_services", P + "_last_delivered_days"):
        init += guard(f"NOT = {{ has_variable = {variable} }}", f"set_variable = {{ {variable} = 0 }}")
    init += f"set_country_flag = {P}_initialized\n"
    effects[P + "_initialize"] = guard(f"{P}_eligible = yes", init)
    effects[P + "_pay_programme"] = (f"clr_country_flag = {P}_payment_authorized\n" + guard(f"{P}_can_fund = yes",
        guard("ac_econ_ready = yes", "ac_econ_pay_programme = yes\n" + guard("OR = { ac_macro_ready = no has_country_flag = ac_macro_transaction_succeeded }", f"set_country_flag = {P}_payment_authorized")) +
        block("else", f"set_country_flag = {P}_payment_authorized") +
        guard(f"has_country_flag = {P}_payment_authorized", "add_political_power = -35\nset_temp_variable = { ac_pol_capacity_delta = -4 }\nac_pol_change_capacity = yes")))
    effects[P + "_refresh_progress"] = guard(f"has_country_flag = {P}_service_active has_variable = {P}_service_started",
        f"set_variable = {{ {P}_elapsed = date }}\nsubtract_from_variable = {{ {P}_elapsed = {P}_service_started }}\nclamp_variable = {{ var = {P}_elapsed min = 0 max = 90 }}")
    cleanup = "".join(f"clr_country_flag = {ident}_active\nremove_ideas = {ident}_spirit\n" for _, _, ident in services)
    effects[P + "_interrupt_service"] = guard(f"{P}_participant = yes has_country_flag = {P}_service_active",
        f"{P}_refresh_progress = yes\nset_variable = {{ {P}_last_delivered_days = {P}_elapsed }}\nset_variable = {{ {P}_last_interrupted_service = {P}_current_service }}\nset_country_flag = {P}_service_interrupted\n" +
        "".join(guard(f"has_country_flag = {ident}_active", f"set_country_flag = {ident}_interrupted") for _, _, ident in services) + cleanup +
        f"clr_country_flag = {P}_service_active\nclr_country_flag = {P}_service_window\nset_variable = {{ {P}_current_service = 0 }}")

    for number_, (branch, n, ident) in enumerate(services, 1):
        title, objective, institution, values = branch.services[n]
        unlock = focus_id(wave, branch, 0 if n == 0 else 3)
        condition = f"{P}_can_fund = yes tag = {branch.tag} original_tag = {branch.tag} has_completed_focus = {unlock}"
        authorize = f"{P}_pay_programme = yes\n" + guard(f"has_country_flag = {P}_payment_authorized",
            f"clr_country_flag = {P}_payment_authorized\nset_country_flag = {P}_service_active\nset_country_flag = {ident}_active\n"
            f"set_country_flag = {{ flag = {P}_service_window days = 90 }}\nset_variable = {{ {P}_current_service = {number_} }}\n"
            f"set_variable = {{ {P}_service_started = date }}\nset_variable = {{ {P}_elapsed = 0 }}\nadd_timed_idea = {{ idea = {ident}_spirit days = 90 }}")
        effects[ident + "_start"] = guard(condition, authorize)
        finish = (f"{P}_active = yes tag = {branch.tag} original_tag = {branch.tag} has_war = no has_country_flag = {P}_service_active "
                  f"has_country_flag = {ident}_active check_variable = {{ {P}_current_service = {number_} }} NOT = {{ has_country_flag = {P}_service_window }}")
        effects[ident + "_finish"] = guard(finish,
            f"remove_ideas = {ident}_spirit\nclr_country_flag = {ident}_active\nclr_country_flag = {P}_service_active\nset_country_flag = {ident}_completed\n"
            f"set_country_flag = {focus_id(wave, branch, 0)[:-len('_register')]}_service_completed\nadd_to_variable = {{ {P}_completed_services = 1 }}\n"
            f"set_variable = {{ {P}_elapsed = 90 }}\nset_variable = {{ {P}_last_delivered_days = 90 }}\nset_variable = {{ {P}_current_service = 0 }}\n"
            f"set_country_flag = {{ flag = {P}_service_cooldown days = 90 }}\n" + branch.service_effect)
        idea(ident + "_spirit", title, institution + " maintains this funded service for ninety days. " + objective +
             " Political authority, institutional capacity and the applicable programme fee were committed at authorization.", values)
        decision(ident, branch.tag, title,
                 objective + "\n\n" + institution + " must complete ninety uninterrupted days. One service may operate nationally; completed periods begin a ninety-day cooldown. "
                 "War, capitulation, annexation or early cancellation ends the period without completion credit. Spent funding is retained. The latest service return appears in the category description.",
                 f"{P}_active = yes has_completed_focus = {unlock}", condition, ident + "_start = yes")

    # Focus branches ------------------------------------------------------
    for branch in wave.branches:
        stem = focus_id(wave, branch, 0)[:-len("_register")]
        for p, (title, benefit, cost) in enumerate(branch.policies):
            ident = focus_id(wave, branch, p + 1) + "_spirit"
            idea(ident, title, branch.descriptions[p + 1], {**benefit, **cost})
            idea(ident + "_settled", title + ": Standing Settlement", branch.descriptions[5] + " The continuing opportunity cost remains.", improve(benefit, cost))
        for index in range(6):
            ident = focus_id(wave, branch, index)
            text(ident, branch.titles[index])
            text(ident + "_desc", branch.descriptions[index])
            x, y = where[ident]
            if index == 0:
                requirement = (("OR = { " + " ".join("has_completed_focus = " + e for e in branch.entry) + " } ") if branch.entry else "") + branch.gate
            elif index in (1, 2):
                requirement = "has_completed_focus = " + focus_id(wave, branch, 0)
            elif index == 3:
                requirement = f"OR = {{ has_completed_focus = {focus_id(wave, branch, 1)} has_completed_focus = {focus_id(wave, branch, 2)} }}"
            elif index == 4:
                requirement = f"has_completed_focus = {focus_id(wave, branch, 3)} has_country_flag = {stem}_service_completed"
            else:
                requirement = "has_completed_focus = " + focus_id(wave, branch, 4)
            condition = f"{P}_active = yes tag = {branch.tag} original_tag = {branch.tag} {requirement}".strip()
            other = focus_id(wave, branch, 2 if index == 1 else 1) if index in (1, 2) else None
            if other:
                condition += f" NOT = {{ has_country_flag = {other}_done }}"
            reward = f"set_country_flag = {ident}_done\n"
            if index == 0:
                reward += f"{P}_narrative_tick = yes\n"
            elif index in (1, 2):
                reward += f"add_ideas = {ident}_spirit\n" + branch.policy_effects[index - 1] + f"{P}_narrative_tick = yes\n"
            elif index == 5:
                for p in (1, 2):
                    policy = focus_id(wave, branch, p)
                    reward += guard(f"has_country_flag = {policy}_done", f"remove_ideas = {policy}_spirit\nadd_ideas = {policy}_spirit_settled")
                reward += branch.settlement_effect + f"{P}_narrative_tick = yes\n"
            effects[ident + "_apply"] = guard(condition + f" NOT = {{ has_country_flag = {ident}_done }}", reward)
            body = f"id = {ident}\nicon = GFX_{P}_focus_{ident}\nx = {x}\ny = {y}\ncost = {10 if index in (1, 2, 5) else 5}\n"
            if index == 0:
                if branch.entry:
                    body += block("prerequisite", "\n".join("focus = " + e for e in branch.entry))
            elif index in (1, 2):
                body += block("prerequisite", "focus = " + focus_id(wave, branch, 0))
            elif index == 3:
                body += block("prerequisite", f"focus = {focus_id(wave, branch, 1)}\nfocus = {focus_id(wave, branch, 2)}")
            else:
                body += block("prerequisite", "focus = " + focus_id(wave, branch, index - 1))
            if other:
                body += block("mutually_exclusive", "focus = " + other)
            body += block("available", condition) + "cancel_if_invalid = yes\ncontinue_if_invalid = no\nai_will_do = { factor = 12 }\n" + block("completion_reward", ident + "_apply = yes")
            focuses.append(block("shared_focus", body))

    text(P + "_funded_cost", "£pol_power 35 / 4 cap")
    # <custom_cost_text>_tooltip and _blocked are the engine's hover and
    # unaffordable variants of a custom decision cost.
    text(P + "_funded_cost_tooltip", "Authorization commits 35 political power and four institutional-capacity points, plus the programme fee shown in the category. Spent resources are not refunded when a period is interrupted.")
    text(P + "_funded_cost_blocked", "£pol_power §R35§! / §R4§! cap")
    text(P + "_fee_macro", "Programme fee: 0.002 billion abstract fiscal units.")
    text(P + "_fee_legacy", "Programme fee: 2 provisional fiscal units.")
    text(P + "_fee_none", "No fiscal fee currently applies. Political and institutional costs remain.")
    for tag, name in wave.countries.items():
        category = f"{P}_{tag.lower()}_services"
        text(category, name + ": " + wave.label)
        # Status, then one line per chosen standing policy (unchosen branches
        # print nothing), then the fee. The cost paragraph is the decisions'
        # own cost tooltip (tools/decision_text measures the result).
        text(category + "_desc", f"[{P}_current_service_text]\n[{P}_cooldown_text]\nService [?{P}_elapsed|0]/90 days, [?{P}_completed_services|0] completed, "
             f"last period [?{P}_last_delivered_days|0] days.\n\n" +
             "".join("[" + branch_id(b) + f"_{P}_policy_line]" for b in wave.branches if b.tag == tag) + f"[{P}_fee_text]")
        categories.append(block(category, f"icon = GFX_{P}_category_{tag.lower()}\nallowed = {{ tag = {tag} original_tag = {tag} }}\nvisible = {{ {P}_eligible = yes }}"))
        decision(f"{tag}_{wave.infix}_cancel_service", tag, "End the Current Service Period",
                 "Release the current rota immediately. Funding and institutional effort already spent are not refunded. Delivered time is retained in the record, but the interrupted period cannot unlock a completed-service review.",
                 f"{P}_active = yes has_country_flag = {P}_service_active", f"{P}_active = yes has_country_flag = {P}_service_active", f"{P}_interrupt_service = yes", cost=False)

    # Narrative -----------------------------------------------------------
    dispatch = []
    interrupted = []

    def event(number_, tag, title, prose, condition, options, picture):
        ident = f"{P}.{number_}"
        token = f"{P}_message_{number_}"
        sent, pending, window, answered = (token + s for s in ("_sent", "_pending", "_window", "_answered"))
        triggers[token + "_answerable"] = f"{P}_active = yes tag = {tag} original_tag = {tag} has_country_flag = {pending} has_country_flag = {window} NOT = {{ has_country_flag = {answered} }}"
        dispatch.append(guard(f"tag = {tag} {P}_active = yes {condition} NOT = {{ has_country_flag = {sent} }}",
            f"set_country_flag = {sent}\nset_country_flag = {pending}\nset_country_flag = {{ flag = {window} days = 60 }}\ncountry_event = {{ id = {ident} days = 1 }}"))
        interrupted.extend(["clr_country_flag = " + pending, "clr_country_flag = " + window])
        text(ident + ".t", title)
        text(ident + ".d", prose)
        body = f"id = {ident}\ntitle = {ident}.t\ndesc = {ident}.d\npicture = {picture}\nis_triggered_only = yes\nfire_only_once = yes\ntrigger = {{ {token}_answerable = yes }}\n"
        for n, (label, action) in enumerate(options):
            option = f"{ident}.{chr(97 + n)}"
            text(option, label)
            apply = f"{token}_reply_{n}"
            effects[apply] = guard(token + "_answerable = yes", f"set_country_flag = {answered}\nclr_country_flag = {pending}\nclr_country_flag = {window}\n" + action)
            body += block("option", f"name = {option}\nai_chance = {{ factor = {55 if n == 0 else 45} }}\n{apply} = yes")
        events.append(block("country_event", body))

    for offset, (tag, name) in enumerate(wave.countries.items()):
        title, prose, labels = wave.openings[tag]
        choices = []
        for n, label in enumerate(labels):
            ident = f"{tag}_{wave.infix}_opening_{'public' if n == 0 else 'ministerial'}"
            values = {"stability_factor": 0.01, "political_power_gain": -0.03} if n == 0 else {"production_factory_efficiency_gain_factor": 0.015, "consumer_goods_factor": 0.005}
            idea(ident + "_spirit", name + (": An Open Hearing" if n == 0 else ": A Ministerial Docket"),
                 "Staff support the chosen opening review for ninety days. Its continuing political attention or civilian reservation remains a real cost.", values)
            choices.append((label, f"set_country_flag = {ident}\nadd_timed_idea = {{ idea = {ident}_spirit days = 90 }}"))
        ready = "OR = { " + " ".join(f"has_country_flag = {focus_id(wave, b, 0)}_done" for b in wave.branches if b.tag == tag) + " }"
        event(event_base + offset, tag, title, prose, ready, choices, f"GFX_{P}_event_{tag.lower()}_national")

    for offset, branch in enumerate(wave.branches):
        bid = branch_id(branch)
        title, prose, labels = branch.scene
        final_title, final_prose = branch.final
        policy_name = f"{bid}_{P}_policy_callback"
        for p in range(2):
            text(f"{policy_name}_{p}", "The standing policy is " + branch.policies[p][0].lower() + ". Its continuing cost remains part of the allocation.")
        custom.append(block("defined_text", "name = " + policy_name + "\n" +
            "".join(block("text", f"trigger = {{ has_country_flag = {focus_id(wave, branch, p + 1)}_done }}\nlocalization_key = {policy_name}_{p}") for p in range(2))))
        choices = []
        for n, label in enumerate(labels):
            ident = f"{focus_id(wave, branch, 0)[:-len('_register')]}_reply_{'public' if n == 0 else 'protected'}"
            values = {k: round(v * .5, 3) for k, v in branch.services[n][3].items()}
            if n == 0:
                if "political_power_gain" in values:
                    values["consumer_goods_factor"] = .005
                else:
                    values["political_power_gain"] = -.03
            else:
                for cost_key, cost in (("stability_factor", -.005), ("consumer_goods_factor", .005), ("political_power_gain", -.03)):
                    if cost_key not in values:
                        values[cost_key] = cost
                        break
            idea(ident + "_spirit", branch.titles[0] + (": Public Return" if n == 0 else ": Protected Working Return"),
                 "This ninety-day response supports the chosen reporting procedure. " + branch.services[n][1] + " Public attention or reserved staff time remains committed to that work.", values)
            choices.append((label, f"set_country_flag = {ident}\nadd_timed_idea = {{ idea = {ident}_spirit days = 90 }}"))
        condition = f"OR = {{ has_country_flag = {focus_id(wave, branch, 1)}_done has_country_flag = {focus_id(wave, branch, 2)}_done }}"
        event(event_base + 10 + offset, branch.tag, title, prose + "\n\n[" + policy_name + "]", condition, choices, f"GFX_{P}_event_{bid}")
        callback = f"{bid}_{P}_report_callback"
        stem = focus_id(wave, branch, 0)[:-len("_register")]
        text(callback + "_public", "The earlier reply opened the return to public questions. The final assessment keeps the unresolved entries visible rather than removing them to produce a cleaner account.")
        text(callback + "_protected", "The earlier reply protected a working return. The final assessment preserves its uncertainties and identifies the office answerable for any later correction.")
        text(callback + "_unanswered", "No first reply was ratified. The final assessment states its reporting duty explicitly instead of inventing a choice that the government never made.")
        response = "".join(block("text", f"trigger = {{ has_country_flag = {stem}_reply_{kind} }}\nlocalization_key = {callback}_{kind}") for kind in ("public", "protected"))
        custom.append(block("defined_text", "name = " + callback + "\n" + response + block("text", f"localization_key = {callback}_unanswered")))
        event(event_base + 40 + offset, branch.tag, final_title, final_prose + "\n\n[" + callback + "]\n\n[" + policy_name + "]",
              f"has_country_flag = {focus_id(wave, branch, 5)}_done", [("File the completed service record.", f"set_country_flag = {stem}_assessment_recorded")], f"GFX_{P}_event_{bid}")

    for offset, (tag, name) in enumerate(wave.countries.items()):
        title, prose, benefit = wave.finals[tag]
        choices = []
        for n, label in enumerate(("Support a public maintenance review.", "Reserve staff for a focused readiness return.")):
            ident = f"{tag}_{wave.infix}_final_{'public' if n == 0 else 'readiness'}"
            values = {"repair_speed_factor": .025, "political_power_gain": -.05} if n == 0 else {**benefit, "consumer_goods_factor": .005}
            idea(ident + "_spirit", name + (": Public Maintenance Assessment" if n == 0 else ": Reserved Readiness Return"),
                 "The final national assessment supports the chosen return for ninety days. Its political or civilian opportunity cost remains, while the enduring policies retain their own continuing tradeoffs.", values)
            choices.append((label, f"set_country_flag = {ident}\nadd_timed_idea = {{ idea = {ident}_spirit days = 90 }}"))
        callback = f"{tag}_{wave.infix}_opening_callback"
        text(callback + "_public", "The opening hearing invited public questions. Its final account returns to that promise without pretending that every disagreement has been resolved.")
        text(callback + "_ministerial", "The opening review began with a protected ministerial docket. Its final account identifies what that process delivered and who must answer for the work still waiting.")
        text(callback + "_unanswered", "The opening invitation was never ratified. This assessment records that absence and proceeds from the services actually completed.")
        entries = "".join(block("text", f"trigger = {{ has_country_flag = {tag}_{wave.infix}_opening_{kind} }}\nlocalization_key = {callback}_{kind}") for kind in ("public", "ministerial"))
        custom.append(block("defined_text", "name = " + callback + "\n" + entries + block("text", f"localization_key = {callback}_unanswered")))
        event(event_base + 70 + offset, tag, title, prose + "\n\n[" + callback + "]", wave.final_ready[tag], choices, f"GFX_{P}_event_{tag.lower()}_national")

    effects[P + "_narrative_tick"] = "\n".join(dispatch)
    effects[P + "_interrupt_narrative"] = guard(f"{P}_participant = yes", "\n".join(interrupted))

    # Defined texts ---------------------------------------------------------
    custom.append(block("defined_text", f"name = {P}_fee_text\n" +
        block("text", f"trigger = {{ ac_macro_ready = yes }}\nlocalization_key = {P}_fee_macro") +
        block("text", f"trigger = {{ ac_econ_ready = yes }}\nlocalization_key = {P}_fee_legacy") +
        block("text", f"localization_key = {P}_fee_none")))
    text(P + "_service_none", "No service period is currently authorized.")
    text(P + "_cooldown_active", "The completed period is in its ninety-day recovery interval.")
    text(P + "_cooldown_ready", "No completed-service cooldown is active.")
    current = "".join(block("text", f"trigger = {{ has_country_flag = {ident}_active }}\nlocalization_key = {ident}") for _, _, ident in services)
    custom.append(block("defined_text", f"name = {P}_current_service_text\n" + current + block("text", f"localization_key = {P}_service_none")))
    custom.append(block("defined_text", f"name = {P}_cooldown_text\n" +
        block("text", f"trigger = {{ has_country_flag = {P}_service_cooldown }}\nlocalization_key = {P}_cooldown_active") +
        block("text", f"localization_key = {P}_cooldown_ready")))
    text(P + "_policy_line_none", "")
    for branch in wave.branches:
        choices = ""
        for index in (1, 2):
            ident = focus_id(wave, branch, index)
            text(ident + "_spirit_settled_policy_line", "Standing policy: " + loc[ident] + " (settled)\n")
            text(ident + "_policy_line", "Standing policy: " + loc[ident] + "\n")
            choices += block("text", f"trigger = {{ has_idea = {ident}_spirit_settled }}\nlocalization_key = {ident}_spirit_settled_policy_line")
            choices += block("text", f"trigger = {{ has_country_flag = {ident}_done }}\nlocalization_key = {ident}_policy_line")
        custom.append(block("defined_text", f"name = {branch_id(branch)}_{P}_policy_line\n" + choices + block("text", f"localization_key = {P}_policy_line_none")))

    # Weekly owner and interruption hooks ---------------------------------
    finish = "\n".join(ident + "_finish = yes" for _, _, ident in services)
    for tag in wave.countries:
        effects[f"{P}_weekly_{tag.lower()}"] = guard(f"tag = {tag} original_tag = {tag}", f"{P}_initialize = yes\n" +
            guard(f"OR = {{ {P}_active = no has_war = yes }}", f"{P}_interrupt_service = yes") +
            guard(f"{P}_active = yes", f"{P}_refresh_progress = yes\n" + finish + f"\n{P}_narrative_tick = yes") +
            wave.weekly_extra.get(tag, ""))
    effects[P + "_interrupt"] = f"{P}_interrupt_service = yes\n{P}_interrupt_narrative = yes\n"
    # Hook bodies by on_action name; the build merges an owner's hooks into the same keys.
    hooks = {"on_startup": "\n".join(f"if = {{ limit = {{ country_exists = {t} }} {t} = {{ {P}_initialize = yes }} }}" for t in wave.countries)}
    for tag in wave.countries:
        hooks[f"on_weekly_{tag}"] = f"{P}_weekly_{tag.lower()} = yes"
    hooks["on_annex"] = f"FROM = {{ {P}_interrupt = yes }}"
    hooks["on_capitulation_immediate"] = f"{P}_interrupt = yes"
    hooks["on_subject_annexed"] = f"{P}_interrupt = yes"
    hooks["on_war_relation_added"] = f"{P}_interrupt_service = yes\nFROM = {{ {P}_interrupt_service = yes }}"

    readable = {P + "_participant": "Established national administration",
                P + "_eligible": "Eligible national continuation",
                P + "_active": "Standing-service administration initialized",
                P + "_idle": "No active service or completed-service cooldown",
                P + "_can_fund": "35 political power, four administrative capacity and the applicable programme fee are available"}
    for key, value in readable.items():
        text(key, value)
    return dict(loc=loc, effects=effects, triggers=triggers, ideas=ideas, focuses=focuses, categories=categories,
                decisions=decisions, custom=custom, events=events, hooks=hooks, services=services, positions=where)


def readable_flags(wave, fragments, script_texts, parse, get):
    """Localize every owned flag so engine tooltips never show raw identifiers."""
    loc = fragments["loc"]
    names = set()

    def nodes(rows):
        for row in rows:
            yield row
            if isinstance(row[2], list):
                yield from nodes(row[2])

    for source in script_texts:
        for key, _, value in nodes(parse(source)):
            if key in ("has_country_flag", "clr_country_flag", "set_country_flag", "has_global_flag", "set_global_flag", "clr_global_flag"):
                names.add(get(value, "flag") if isinstance(value, list) else value)
    tags = tuple(wave.countries) + tuple(wave.extra_tags)
    owned = re.compile(r"^(?:" + re.escape(wave.prefix) + "_" + (r"|(?:" + "|".join(tags) + ")_" + wave.infix + "_" if tags else "") + ")")
    for flag in sorted(n for n in names if n):
        if flag in loc or not owned.match(flag):
            continue
        known = None
        for branch in wave.branches:
            for index in range(6):
                if flag == focus_id(wave, branch, index) + "_done":
                    known = loc[focus_id(wave, branch, index)] + ": completed"
        loc[flag] = known or (wave.label + ": " + owned.sub("", flag).replace("_", " ").capitalize())
