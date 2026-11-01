"""Compile sixty additive national continuations and their owned service runtime.

All effects are provisional gameplay. No history, leader, army, territory,
authoritative war/faction/project state, or private shared-owner balance is owned.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]; MOD = ROOT / "mod/2985041246"
sys.path.insert(0, str(ROOT / "tools"))
from reconstruction.content import BRANCHES, COUNTRY_NAMES, SUFFIXES, branch_id, focus_id
from usea_expansion.script import parse, get, walk
from port_1_19.pdx import children, strip_comments_mask

NOTE = "# Original provisional gameplay; source: tools/reconstruction. Native acceptance pending.\n"
BEGIN, END = "# BEGIN RECONSTRUCTION CONTINUATIONS", "# END RECONSTRUCTION CONTINUATIONS"
LAYOUT = {"NPT": ([20, 29, 38], 12, 3168), "REC": ([20, 29, 38], 9, 3168),
          "SAP": ([70, 79], 10, 7008), "GEB": ([60, 69], 17, 6048)}
TREE_IDS = {"NPT": "npt_pre_continental_war_focus", "REC": "rec_postwar_consolidation_focus",
            "SAP": "sap_focus", "GEB": "geb_pre_belkan_war_focus"}
SERVICES = [(b, n, f"{branch_id(b)}_service_{n+1}") for b in BRANCHES for n in range(2)]


def block(key, body):
    return key + " = {\n" + "\n".join("\t" + line if line else "" for line in body.splitlines()) + "\n}\n"


def guard(condition, body):
    return block("if", block("limit", condition) + body)


def modifiers(values):
    return "\n".join(key + " = " + format(value, ".3f").rstrip("0").rstrip(".") for key, value in values.items())


def ready_date():
    return "date > 2005.12.31"


def entry_condition(branch):
    completed = "has_completed_focus = " + branch.entry
    if branch.tag in ("SAP", "GEB"):
        return "OR = { " + completed + " AND = { has_war = no NOT = { has_global_flag = ac_postwar_contract_started } " + ready_date() + " } }"
    return completed


def requirements(branch, index):
    if index == 0: return entry_condition(branch)
    if index in (1, 2): return "has_completed_focus = " + focus_id(branch, 0)
    if index == 3: return "OR = { has_completed_focus = " + focus_id(branch, 1) + " has_completed_focus = " + focus_id(branch, 2) + " }"
    return "has_completed_focus = " + focus_id(branch, index - 1) + (" has_country_flag = " + branch_id(branch) + "_service_completed" if index == 4 else "")


def improve(benefits, costs):
    return {**{key: round(value * 1.2, 3) for key, value in benefits.items()}, **costs}


def focus_positions():
    result = {}; offsets = defaultdict(int)
    for branch in BRANCHES:
        roots, y, _ = LAYOUT[branch.tag]; x = roots[offsets[branch.tag]]; offsets[branch.tag] += 1
        for index in range(6):
            result[focus_id(branch, index)] = (x + (-2 if index == 1 else 2 if index == 2 else 0), y + (0 if index == 0 else index - 1 if index > 2 else 1))
    return result


def attach(source, tag):
    """Replace only the owned import block; preserve every foreign source byte."""
    if source.count(BEGIN) != source.count(END) or source.count(BEGIN) > 1:
        raise ValueError("Unbalanced reconstruction import ownership: " + tag)
    if BEGIN in source:
        start = source.index(BEGIN); finish = source.index(END) + len(END)
        owned = parse(source[start:finish])
        expected = {focus_id(b, i) for b in BRANCHES if b.tag == tag for i in range(6)}
        if any(k != "shared_focus" or v not in expected for k, _, v in owned):
            raise ValueError("Foreign content inside reconstruction import block: " + tag)
        replacement = BEGIN + "\n" + "".join("\tshared_focus = " + focus_id(b, i) + "\n" for b in BRANCHES if b.tag == tag for i in range(6)) + "\t" + END
        source = source[:start] + replacement + source[finish:]
        # Keep this section's position stable relative to other generators.
        existing = True
    else: existing = False
    mask = strip_comments_mask(source)
    trees = [row for row in children(source, 0, len(source), mask) if row[0] == "focus_tree"]
    matches = [row for row in trees if re.search(r"\bid\s*=\s*" + re.escape(TREE_IDS[tag]) + r"\b", source[row[3]:row[4]])]
    if len(matches) != 1: raise ValueError("Expected stable national tree: " + tag)
    _, _, _, start, end = matches[0]
    body = source[start:end]
    position = re.search(r"continuous_focus_position\s*=\s*\{[^{}]*\}", body)
    if not position: raise ValueError("Missing existing continuous-focus position: " + tag)
    replacement = f"continuous_focus_position = {{ x = {LAYOUT[tag][2]} y = 16 }}"
    body = body[:position.start()] + replacement + body[position.end():]
    imports = "\n\t" + BEGIN + "\n" + "".join("\tshared_focus = " + focus_id(b, i) + "\n" for b in BRANCHES if b.tag == tag for i in range(6)) + "\t" + END + "\n"
    return source[:start] + (body if existing else body.rstrip() + "\n" + imports) + source[end:]


def outputs():
    out = {}; loc = {}; effects = {}; triggers = {}; ideas = []; focuses = []; categories = []; decisions = defaultdict(list)
    positions = focus_positions()
    def text(key, value):
        if key in loc: raise ValueError("Duplicate reconstruction localization: " + key)
        loc[key] = value
    def idea(ident, title, description, values):
        text(ident, title); text(ident + "_desc", description)
        ideas.append(block(ident, "picture = " + ident + "\nallowed = { always = no }\nallowed_civil_war = { always = no }\nremoval_cost = -1\n" + block("modifier", modifiers(values))))
    def decision(ident, tag, title, description, visible, available, action, cost=True):
        text(ident, title); text(ident + "_desc", description)
        body = f"icon = ac_rc_{ident}\nallowed = {{ tag = {tag} original_tag = {tag} }}\nvisible = {{ {visible} }}\navailable = {{ {available} }}\ncost = 0\n"
        if cost: body += "custom_cost_trigger = { ac_rc_can_fund = yes }\ncustom_cost_text = ac_rc_funded_cost\n"
        body += block("complete_effect", action) + "ai_will_do = { base = " + ("3" if cost else "0") + " }\n"
        decisions["ac_rc_" + tag.lower() + "_services"].append(block(ident, body))

    participant = "OR = { " + " ".join("AND = { tag = " + tag + " original_tag = " + tag + " }" for tag in COUNTRY_NAMES) + " }"
    triggers["ac_rc_participant"] = participant
    triggers["ac_rc_eligible"] = "ac_rc_participant = yes any_owned_state = { always = yes } has_capitulated = no " + ready_date()
    triggers["ac_rc_active"] = "ac_rc_eligible = yes has_country_flag = ac_rc_initialized"
    triggers["ac_rc_idle"] = "NOT = { has_country_flag = ac_rc_service_active } check_variable = { ac_rc_current_service = 0 } NOT = { has_country_flag = ac_rc_service_cooldown }"
    triggers["ac_rc_can_fund"] = "ac_rc_active = yes has_war = no ac_rc_idle = yes political_power >= 35 ac_pol_active = yes check_variable = { ac_pol_capacity >= 4 } OR = { ac_econ_enabled = no ac_econ_can_pay_programme = yes }"
    initialize = ""
    for variable in ("ac_rc_current_service", "ac_rc_elapsed", "ac_rc_completed_services", "ac_rc_last_delivered_days"):
        initialize += guard("NOT = { has_variable = " + variable + " }", "set_variable = { " + variable + " = 0 }")
    initialize += "set_country_flag = ac_rc_initialized\n"
    effects["ac_rc_initialize"] = guard("ac_rc_eligible = yes", initialize)
    effects["ac_rc_pay_programme"] = "clr_country_flag = ac_rc_payment_authorized\n" + guard("ac_rc_can_fund = yes",
        guard("ac_econ_ready = yes", "ac_econ_pay_programme = yes\n" + guard("OR = { ac_macro_ready = no has_country_flag = ac_macro_transaction_succeeded }", "set_country_flag = ac_rc_payment_authorized")) +
        block("else", "set_country_flag = ac_rc_payment_authorized") +
        guard("has_country_flag = ac_rc_payment_authorized", "add_political_power = -35\nset_temp_variable = { ac_pol_capacity_delta = -4 }\nac_pol_change_capacity = yes"))
    effects["ac_rc_refresh_progress"] = guard("has_country_flag = ac_rc_service_active has_variable = ac_rc_service_started",
        "set_variable = { ac_rc_elapsed = date }\nsubtract_from_variable = { ac_rc_elapsed = ac_rc_service_started }\nclamp_variable = { var = ac_rc_elapsed min = 0 max = 90 }")
    cleanup = "".join("clr_country_flag = " + ident + "_active\nremove_ideas = " + ident + "_spirit\n" for _, _, ident in SERVICES)
    effects["ac_rc_interrupt_service"] = guard("ac_rc_participant = yes has_country_flag = ac_rc_service_active",
        "ac_rc_refresh_progress = yes\nset_variable = { ac_rc_last_delivered_days = ac_rc_elapsed }\nset_variable = { ac_rc_last_interrupted_service = ac_rc_current_service }\nset_country_flag = ac_rc_service_interrupted\n" +
        "\n".join(guard("has_country_flag = " + ident + "_active", "set_country_flag = " + ident + "_interrupted") for _, _, ident in SERVICES) + cleanup +
        "clr_country_flag = ac_rc_service_active\nclr_country_flag = ac_rc_service_window\nset_variable = { ac_rc_current_service = 0 }")
    for number, (branch, n, ident) in enumerate(SERVICES, 1):
        title, objective, institution, values = branch.services[n]
        unlock = focus_id(branch, 0 if n == 0 else 3)
        condition = f"ac_rc_can_fund = yes tag = {branch.tag} original_tag = {branch.tag} has_completed_focus = {unlock}"
        authorize = "ac_rc_pay_programme = yes\n" + guard("has_country_flag = ac_rc_payment_authorized",
            f"clr_country_flag = ac_rc_payment_authorized\nset_country_flag = ac_rc_service_active\nset_country_flag = {ident}_active\nset_country_flag = {{ flag = ac_rc_service_window days = 90 }}\nset_variable = {{ ac_rc_current_service = {number} }}\nset_variable = {{ ac_rc_service_started = date }}\nset_variable = {{ ac_rc_elapsed = 0 }}\nadd_timed_idea = {{ idea = {ident}_spirit days = 90 }}")
        effects[ident + "_start"] = guard(condition, authorize)
        finish = f"ac_rc_active = yes tag = {branch.tag} original_tag = {branch.tag} has_war = no has_country_flag = ac_rc_service_active has_country_flag = {ident}_active check_variable = {{ ac_rc_current_service = {number} }} NOT = {{ has_country_flag = ac_rc_service_window }}"
        effects[ident + "_finish"] = guard(finish,
            f"remove_ideas = {ident}_spirit\nclr_country_flag = {ident}_active\nclr_country_flag = ac_rc_service_active\nset_country_flag = {ident}_completed\nset_country_flag = {branch_id(branch)}_service_completed\nadd_to_variable = {{ ac_rc_completed_services = 1 }}\nset_variable = {{ ac_rc_elapsed = 90 }}\nset_variable = {{ ac_rc_last_delivered_days = 90 }}\nset_variable = {{ ac_rc_current_service = 0 }}\nset_country_flag = {{ flag = ac_rc_service_cooldown days = 90 }}")
        idea(ident + "_spirit", title, institution + " maintains this funded service for ninety days. " + objective + " Political authority, institutional capacity and the applicable programme fee were committed at authorization.", values)
        decision(ident, branch.tag, title,
            objective + "\n\n" + institution + " must complete ninety uninterrupted days. One service may operate nationally; completed periods begin a ninety-day cooldown. War, capitulation, annexation or early cancellation ends the period without completion credit. Spent funding is retained. The latest service return appears above.",
            f"ac_rc_active = yes has_completed_focus = {unlock}", condition, ident + "_start = yes")

    for branch in BRANCHES:
        bid = branch_id(branch)
        for p, (title, benefit, cost) in enumerate(branch.policies):
            ident = focus_id(branch, p + 1) + "_spirit"
            description = branch.descriptions[p + 1]
            idea(ident, title, description, {**benefit, **cost})
            idea(ident + "_settled", title + ": Standing Settlement", branch.descriptions[5] + " The continuing opportunity cost remains.", improve(benefit, cost))
        for index in range(6):
            ident = focus_id(branch, index); text(ident, branch.titles[index]); text(ident + "_desc", branch.descriptions[index])
            x, y = positions[ident]; condition = f"ac_rc_active = yes tag = {branch.tag} original_tag = {branch.tag} " + requirements(branch, index)
            other = focus_id(branch, 2 if index == 1 else 1) if index in (1, 2) else None
            if other: condition += " NOT = { has_country_flag = " + other + "_done }"
            reward = "set_country_flag = " + ident + "_done\n"
            if index == 0: reward += "ac_rc_narrative_tick = yes\n"
            elif index in (1, 2): reward += "add_ideas = " + ident + "_spirit\nac_rc_narrative_tick = yes\n"
            elif index == 5:
                for p in (1, 2):
                    policy = focus_id(branch, p)
                    reward += guard("has_country_flag = " + policy + "_done", "remove_ideas = " + policy + "_spirit\nadd_ideas = " + policy + "_spirit_settled")
                reward += "ac_rc_narrative_tick = yes\n"
            effects[ident + "_apply"] = guard(condition + " NOT = { has_country_flag = " + ident + "_done }", reward)
            body = f"id = {ident}\nicon = GFX_ac_rc_focus_{ident}\nx = {x}\ny = {y}\ncost = {10 if index in (1,2,5) else 5}\n"
            if index == 0:
                if branch.tag not in ("SAP", "GEB"): body += block("prerequisite", "focus = " + branch.entry)
            elif index in (1, 2): body += block("prerequisite", "focus = " + focus_id(branch, 0))
            elif index == 3: body += block("prerequisite", "focus = " + focus_id(branch, 1) + "\nfocus = " + focus_id(branch, 2))
            else: body += block("prerequisite", "focus = " + focus_id(branch, index - 1))
            if other: body += block("mutually_exclusive", "focus = " + other)
            body += block("available", condition) + "cancel_if_invalid = yes\ncontinue_if_invalid = no\nai_will_do = { factor = 12 }\n" + block("completion_reward", ident + "_apply = yes")
            focuses.append(block("shared_focus", body))
    text("ac_rc_funded_cost", "£pol_power 35 / 4 cap")
    text("ac_rc_funded_cost_tt", "Authorization commits 35 political power and four institutional-capacity points, plus the applicable programme fee below. Spent resources are not refunded when a period is interrupted.")
    text("ac_rc_fee_macro", "Programme fee: 0.002 billion abstract fiscal units.")
    text("ac_rc_fee_legacy", "Programme fee: 2 provisional fiscal units.")
    text("ac_rc_fee_none", "No fiscal fee currently applies. Political and institutional costs remain.")
    for tag, name in COUNTRY_NAMES.items():
        category = "ac_rc_" + tag.lower() + "_services"
        text(category, name + ": Standing Services")
        text(category + "_desc", "[ac_rc_current_service_text]\n[ac_rc_cooldown_text]\nLatest service return: [?ac_rc_elapsed|0]/90 days. Completed periods: [?ac_rc_completed_services|0]. Last interrupted or completed period delivered [?ac_rc_last_delivered_days|0] days.\n\n" +
             "\n".join(b.titles[0] + ": [" + branch_id(b) + "_policy_text]" for b in BRANCHES if b.tag == tag) + "\n\n" + loc["ac_rc_funded_cost_tt"] + "\n[ac_rc_fee_text]")
        categories.append(block(category, f"icon = GFX_ac_rc_category_{tag.lower()}\nallowed = {{ tag = {tag} original_tag = {tag} }}\nvisible = {{ ac_rc_eligible = yes }}"))
        decision(tag + "_rc_cancel_service", tag, "End the Current Service Period",
            "Release the current rota immediately. Funding and institutional effort already spent are not refunded. Delivered time is retained in the record, but the interrupted period cannot unlock a completed-service review.",
            "ac_rc_active = yes has_country_flag = ac_rc_service_active", "ac_rc_active = yes has_country_flag = ac_rc_service_active", "ac_rc_interrupt_service = yes", cost=False)

    from reconstruction.narrative import build_narrative
    narrative, custom = build_narrative(effects, triggers, text, idea)
    custom += block("defined_text", "name = ac_rc_fee_text\n" +
        block("text", "trigger = { ac_macro_ready = yes }\nlocalization_key = ac_rc_fee_macro") +
        block("text", "trigger = { ac_econ_ready = yes }\nlocalization_key = ac_rc_fee_legacy") +
        block("text", "localization_key = ac_rc_fee_none"))
    text("ac_rc_service_none", "No service period is currently authorized.")
    text("ac_rc_cooldown_active", "The completed period is in its ninety-day recovery interval.")
    text("ac_rc_cooldown_ready", "No completed-service cooldown is active.")
    current = ""
    for _, _, ident in SERVICES:
        current += block("text", "trigger = { has_country_flag = " + ident + "_active }\nlocalization_key = " + ident)
    custom += block("defined_text", "name = ac_rc_current_service_text\n" + current + block("text", "localization_key = ac_rc_service_none"))
    custom += block("defined_text", "name = ac_rc_cooldown_text\n" + block("text", "trigger = { has_country_flag = ac_rc_service_cooldown }\nlocalization_key = ac_rc_cooldown_active") + block("text", "localization_key = ac_rc_cooldown_ready"))
    for branch in BRANCHES:
        choices = ""
        for index in (1, 2):
            ident = focus_id(branch, index)
            choices += block("text", "trigger = { has_idea = " + ident + "_spirit_settled }\nlocalization_key = " + ident + "_spirit_settled")
            choices += block("text", "trigger = { has_country_flag = " + ident + "_done }\nlocalization_key = " + ident)
        none = branch_id(branch) + "_policy_none"; text(none, "A standing policy has not yet been selected.")
        custom += block("defined_text", "name = " + branch_id(branch) + "_policy_text\n" + choices + block("text", "localization_key = " + none))
    finish = "\n".join(ident + "_finish = yes" for _, _, ident in SERVICES)
    effects["ac_rc_weekly"] = guard("ac_rc_participant = yes", "ac_rc_initialize = yes\n" +
        guard("OR = { ac_rc_active = no has_war = yes }", "ac_rc_interrupt_service = yes") +
        guard("ac_rc_active = yes", "ac_rc_refresh_progress = yes\n" + finish + "\nac_rc_narrative_tick = yes"))
    effects["ac_rc_interrupt"] = "ac_rc_interrupt_service = yes\nac_rc_interrupt_narrative = yes\n"
    hooks = block("on_startup", block("effect", "\n".join(tag + " = { ac_rc_initialize = yes }" for tag in COUNTRY_NAMES)))
    hooks += block("on_weekly", block("effect", "ac_rc_weekly = yes"))
    hooks += block("on_annex", block("effect", "FROM = { ac_rc_interrupt = yes }"))
    hooks += block("on_capitulation_immediate", block("effect", "ac_rc_interrupt = yes"))
    hooks += block("on_subject_annexed", block("effect", "ac_rc_interrupt = yes"))
    hooks += block("on_war_relation_added", block("effect", "ac_rc_interrupt_service = yes\nFROM = { ac_rc_interrupt_service = yes }"))
    out["common/national_focus/ac_reconstruction_continuations.txt"] = NOTE + "\n".join(focuses)
    for tag in COUNTRY_NAMES:
        relative = "common/national_focus/" + tag + ".txt"
        out[relative] = attach((MOD / relative).read_text(encoding="utf-8-sig"), tag)
    out["common/scripted_effects/ac_reconstruction.txt"] = NOTE + "\n".join(block(k,v) for k,v in effects.items())
    out["common/scripted_triggers/ac_reconstruction.txt"] = NOTE + "\n".join(block(k,v) for k,v in triggers.items())
    out["common/ideas/ac_reconstruction.txt"] = NOTE + block("ideas", block("country", "\n".join(ideas)))
    out["common/decisions/categories/ac_reconstruction.txt"] = NOTE + "\n".join(categories)
    out["common/decisions/ac_reconstruction.txt"] = NOTE + "\n".join(block(k,"\n".join(v)) for k,v in decisions.items())
    out["common/on_actions/ac_reconstruction.txt"] = NOTE + block("on_actions", hooks)
    out["common/custom_localization/ac_reconstruction.txt"] = NOTE + custom
    out["events/ac_reconstruction.txt"] = NOTE + "add_namespace = ac_rc\n" + narrative
    # Engine prerequisite/effect tooltips may expose these internal conditions.
    # Keep every owned flag readable without treating it as a separate policy.
    readable = {"ac_rc_participant":"Established national administration", "ac_rc_eligible":"Eligible domestic continuation after 2005",
        "ac_rc_active":"Standing-service administration initialized", "ac_rc_idle":"No active service or completed-service cooldown",
        "ac_rc_can_fund":"35 political power, four administrative capacity and the applicable programme fee are available"}
    for key,value in readable.items():text(key,value)
    flag_names=set()
    def all_nodes(nodes):
        for row in nodes:
            yield row
            if isinstance(row[2],list):yield from all_nodes(row[2])
    for relative,source in out.items():
        if relative.endswith('.txt'):
            for key,_,value in all_nodes(parse(source)):
                if key in ('has_country_flag','clr_country_flag','set_country_flag'):
                    flag_names.add(get(value,'flag') if isinstance(value,list) else value)
    for flag in sorted(flag_names):
        if flag and flag not in loc and (flag.startswith('ac_rc_') or re.match(r'^(NPT|REC|SAP|GEB)_rc_',flag)):
            known=next((loc[focus_id(b,i)] + ': completed' for b in BRANCHES for i in range(6) if flag==focus_id(b,i)+'_done'),None)
            text(flag,known or 'Standing services: '+re.sub(r'^(?:ac_rc_|(?:NPT|REC|SAP|GEB)_rc_)','',flag).replace('_',' ').capitalize())
    out["localisation/english/ac_reconstruction_l_english.yml"] = "\ufeffl_english:\n" + "\n".join(' ' + k + ':0 "' + v.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n') + '"' for k,v in loc.items()) + "\n"
    return out


def inventory():
    positions = focus_positions()
    return dict(schema=1, source_layer="Original provisional gameplay; all domestic procedures are authored alternatives",
        focuses=[dict(id=focus_id(b,i), tag=b.tag, branch=b.key, title=b.titles[i], x=positions[focus_id(b,i)][0], y=positions[focus_id(b,i)][1],
                      purpose=("Unlock service1" if i==0 else "Exclusive enduring policy" if i in (1,2) else "Unlock service2" if i==3 else "Require a completed ninety-day period" if i==4 else "Improve the chosen policy while retaining its cost")) for b in BRANCHES for i in range(6)],
        services=[dict(id=ident,tag=b.tag,branch=b.key,days=90,cooldown_days=90,political_power=35,capacity=4,legacy_fee=2,macro_fee_billion=0.002) for b,n,ident in SERVICES],
        continuity="No history or calendar grant; after2020 conclusions remain available. Existing tree/focus/event/outcome owners remain authoritative.")


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--check",action="store_true");args=parser.parse_args()
    failures=[]
    for relative,text in outputs().items():
        path=MOD/relative
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8")!=text:failures.append(relative)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding="utf-8",newline="\n")
    text=json.dumps(inventory(),indent=2)+"\n";path=HERE/"manifest.json"
    if args.check:
        if not path.exists() or path.read_text()!=text:failures.append("tools/reconstruction/manifest.json")
    else:path.write_text(text,encoding="utf-8",newline="\n")
    if failures:raise SystemExit("Reconstruction output differs: "+", ".join(failures))
    print("Reconstruction:60 focus definitions,20 funded services; "+("consistent" if args.check else "generated"))


if __name__ == "__main__":main()
