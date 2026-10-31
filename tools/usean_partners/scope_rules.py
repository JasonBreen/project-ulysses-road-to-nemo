"""Paid operational scopes consume actual national service records/capacity."""
from scopes import SCOPES
from usean_partner_builder import block, guard, loc, emit

RESOURCES = {
    "contacts": ("ac_up_sns_contact_records", "verified continuity record"),
    "protection": ("ac_up_sns_protection_records", "verified protection record"),
    "slots": ("ac_up_amber_slots", "funded spare service slot"),
    "cases": ("ac_up_del_cases", "verified inspection case"),
}


def build_scope_rules(effects, triggers, decisions):
    triggers["ac_up_scope_idle"] = "NOT = { has_country_flag = ac_up_scope_active }"
    loc("ac_up_scope_active", "A funded operational scope remains active")
    loc("ac_up_scope_window", "The current 90-day scope allocation remains in progress")
    ideas = []; tick = ""; suspend = ""
    for scope in SCOPES:
        ident = scope.id
        conditions = "ac_up_active = yes tag = " + scope.tag + " ac_up_can_fund = yes ac_up_scope_idle = yes NOT = { has_country_flag = ac_up_scope_window } "
        conditions += " ".join("has_country_flag = " + scope.tag + "_up_" + suffix + "_done" for suffix in scope.requirements)
        if scope.resource == "occupied_slot":
            conditions += " check_variable = { ac_up_uge_used < ac_up_uge_limit }"
            resource_text = "Occupies one simultaneous service slot for 90 days, competing with the existing leases. The slot returns once on expiry; interruption forfeits spent political and fiscal costs."
            resource_effect = "add_to_variable = { ac_up_uge_used = 1 }"
        else:
            variable, label = RESOURCES[scope.resource]
            conditions += " check_variable = { " + variable + " > 0 }"
            resource_text = "Consumes one " + label + ". The record or slot is not refunded, including after interruption."
            resource_effect = "add_to_variable = { " + variable + " = -1 }"
        loc(ident, scope.title)
        loc(ident + "_desc", scope.purpose + "\n\n" + resource_text + " One operational scope may run at a time. Its benefits and opportunity costs last 90 days. All listed focus capabilities are required; they are distinct parts of this service rather than interchangeable capacity points.")
        loc(ident + "_spirit", scope.title); loc(ident + "_spirit_desc", scope.purpose + " " + resource_text)
        ideas.append(block(ident + "_spirit", "picture = ac_up_idea_" + ident + "_spirit\nallowed = { always = no }\nallowed_civil_war = { always = no }\nremoval_cost = -1\n" + block("modifier", scope.modifier)))
        body = "ac_up_pay_programme = yes\n" + resource_effect + "\nset_country_flag = ac_up_scope_active\nset_country_flag = " + ident + "_active\nset_country_flag = { flag = ac_up_scope_window days = 90 }\nadd_ideas = " + ident + "_spirit\nac_up_bound = yes"
        effects[ident + "_start"] = guard(conditions, body)
        cleanup = "clr_country_flag = ac_up_scope_active\nclr_country_flag = " + ident + "_active\nremove_ideas = " + ident + "_spirit\n"
        if scope.resource == "occupied_slot":
            cleanup += "add_to_variable = { ac_up_uge_used = -1 }\n"
        effects[ident + "_finish"] = guard("ac_up_active = yes tag = " + scope.tag + " has_country_flag = " + ident + "_active NOT = { has_country_flag = ac_up_scope_window }", cleanup + "ac_up_bound = yes")
        tick += ident + "_finish = yes\n"
        suspend += "clr_country_flag = " + ident + "_active\nremove_ideas = " + ident + "_spirit\n"
        preview = "custom_effect_tooltip = ac_up_cost_tt\n" + block("effect_tooltip", "add_ideas = " + ident + "_spirit")
        decision = f"icon = ac_up_{scope.tag.lower()}_programme\nallowed = {{ tag = {scope.tag} original_tag = {scope.tag} }}\nvisible = {{ ac_up_active = yes }}\navailable = {{ {conditions} }}\ncost = 0\n"
        decision += block("complete_effect", preview + block("hidden_effect", ident + "_start = yes")) + "ai_will_do = { base = 2 }\n"
        decisions["ac_up_" + scope.tag.lower() + "_programmes"].append(block(ident, decision))
    effects["ac_up_scope_tick"] = tick
    effects["ac_up_scope_suspend"] = suspend + "clr_country_flag = ac_up_scope_active\nclr_country_flag = ac_up_scope_window\n"
    emit("common/ideas/ac_usean_partner_scopes.txt", block("ideas", block("country", "\n".join(ideas))))
