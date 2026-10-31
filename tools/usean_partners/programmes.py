"""Distinct national programme rules and four bounded reciprocal FCU offers."""
from content import COUNTRIES
from usean_partner_builder import block, guard, loc, emit, earned, OFFER_UNLOCKS, EVENTS


def decision(tag, suffix, title, desc, condition, action, visible="ac_up_active = yes", weight=2):
    ident = tag + "_up_" + suffix
    loc(ident, title); loc(ident + "_desc", desc)
    preview = "" if suffix.startswith("release_") else "custom_effect_tooltip = ac_up_cost_tt\n"
    return block(ident, f"icon = ac_up_{tag.lower()}_programme\nallowed = {{ tag = {tag} original_tag = {tag} }}\nvisible = {{ {visible} }}\navailable = {{ {condition} }}\ncost = 0\n" + block("complete_effect", preview + block("hidden_effect", action)) + f"ai_will_do = {{ base = {weight} }}")


def build_country_rules(effects, triggers, decisions):
    # Finite national resources are not a second political-capacity owner.
    # Every paid action rechecks the shared owner before charging or rewarding.
    reviews = {
        "SNS": ("review_burden", "Review the Civil Protection Burden",
                "Fund an accountable review of local protection work. An intact Stonehenge complex adds a project liaison task; after its loss the same staff review domestic continuity. This never changes the project's ownership or operational state.",
                "ac_up_can_fund = yes OR = { has_country_flag = SNS_up_project_burden_review_done has_country_flag = SNS_up_stonehenge_liaison_done has_country_flag = SNS_up_protection_accounts_done } NOT = { has_country_flag = ac_up_review_cooldown }",
                "ac_up_pay_programme = yes\nset_country_flag = { flag = ac_up_review_cooldown days = 180 }\nadd_to_variable = { ac_up_sns_protection = 2 }\n" + guard("ac_ucw_stonehenge_intact = yes", "add_to_variable = { ac_up_sns_dispatch = 2 }") + block("else", "add_to_variable = { ac_up_sns_continuity = 2 }") + "ac_up_recovery_credit = yes"),
        "AMB": ("reassign_slot", "Reassign a Spare Slot to Domestic Work",
                "Spend one funded spare slot on a domestic receiving task instead of a coalition offer. The ordinary programme costs still apply. This is a useful fallback when cooperation is refused or unavailable.",
                "ac_up_can_fund = yes has_country_flag = AMB_up_spare_capacity_done check_variable = { ac_up_amber_slots > 0 } NOT = { has_country_flag = ac_up_review_cooldown }",
                "ac_up_pay_programme = yes\nadd_to_variable = { ac_up_amber_slots = -1 }\nset_country_flag = { flag = ac_up_review_cooldown days = 180 }\nadd_to_variable = { ac_up_amb_transport = 3 }\nac_up_recovery_credit = yes"),
        "DEL": ("resolve_docket", "Resolve a Verified Command Docket",
                "Use a verified inspection case to resolve one outstanding command obligation. The review pays its normal programme cost, then restores one point of institutional capacity through the owning framework. It does not create a new command mandate.",
                "ac_up_can_fund = yes has_country_flag = DEL_up_verification_rules_done check_variable = { ac_up_del_cases > 0 } check_variable = { ac_up_del_obligations > 0 } NOT = { has_country_flag = ac_up_review_cooldown }",
                "ac_up_pay_programme = yes\nadd_to_variable = { ac_up_del_cases = -1 }\nadd_to_variable = { ac_up_del_obligations = -1 }\nset_country_flag = { flag = ac_up_review_cooldown days = 90 }\nset_temp_variable = { ac_pol_capacity_delta = 1 }\nac_pol_change_capacity = yes\nadd_to_variable = { ac_up_del_oversight = 2 }"),
    }
    for tag, (suffix, title, desc, condition, body) in reviews.items():
        ident = tag + "_up_" + suffix
        effects[ident + "_apply"] = guard("tag = " + tag + " " + condition, body + "\nac_up_bound = yes\nac_up_recalculate = yes")
        decisions["ac_up_" + tag.lower() + "_programmes"].append(decision(tag, suffix, title, desc, condition, ident + "_apply = yes"))
    # Ugellas can abandon one lease at a time to free scarce capacity. Cost and
    # completion credit are forfeited; releasing an already ended lease is inert.
    from usean_partner_builder import LEASES
    for kind, title, *_ in LEASES["UGE"]:
        ident = "UGE_up_" + kind + "_programme"
        condition = f"ac_up_active = yes has_country_flag = {ident}_active"
        body = f"clr_country_flag = {ident}_active\nclr_country_flag = {ident}_window\nremove_ideas = {ident}_spirit\nadd_to_variable = {{ ac_up_uge_used = -1 }}\nac_up_bound = yes"
        effects[ident + "_release"] = guard("tag = UGE " + condition, body)
        decisions["ac_up_uge_programmes"].append(decision("UGE", "release_" + kind, "Release: " + title,
            "Release this service commitment to free its occupied slot. Its political, administrative and fiscal costs are not refunded, and no completion credit is awarded. Another lease still requires a new funded allocation.", condition, ident + "_release = yes", weight=0))
    build_offers(effects, triggers, decisions)


def build_offers(effects, triggers, decisions):
    sender_ticks = ""; recipient_cleanup = ""; interruption = ""
    for offset, (tag, cfg) in enumerate(COUNTRIES.items()):
        lower = tag.lower(); pending = "ac_up_" + lower + "_pending"
        window = "ac_up_" + lower + "_offer_window"
        valid = "ac_up_" + lower + "_partner_valid"
        triggers[valid] = f"tag = {tag} original_tag = {tag} has_capitulated = no is_subject = no country_exists = FCU NOT = {{ has_war_with = FCU }} FCU = {{ tag = FCU original_tag = FCU has_capitulated = no is_subject = no }}"
        condition = f"ac_up_can_fund = yes {earned(tag, OFFER_UNLOCKS[tag])} {valid} = yes NOT = {{ has_country_flag = ac_up_offer_attempted }}"
        if tag == "AMB":
            condition += " check_variable = { ac_up_amber_slots > 0 }"
        action = "ac_up_pay_programme = yes\nset_country_flag = ac_up_offer_attempted\nset_country_flag = ac_up_offer_pending\nset_country_flag = { flag = " + window + " days = 60 }\n"
        action += guard("has_country_flag = ac_up_offer_priority ac_pol_active = yes", "clr_country_flag = ac_up_offer_priority\nset_temp_variable = { ac_pol_capacity_delta = 1 }\nac_pol_change_capacity = yes")
        if tag == "AMB":
            action += "add_to_variable = { ac_up_amber_slots = -1 }\nset_country_flag = ac_up_offer_slot_committed\n"
        action += f"FCU = {{ set_country_flag = {pending} country_event = {{ id = ac_up.{101 + offset} days = 1 }} }}"
        effects[tag + "_up_send_offer"] = guard("tag = " + tag + " " + condition, action)
        decisions["ac_up_" + lower + "_programmes"].append(decision(tag, "offer_service", "Offer a Bounded Service to Central Usea",
            "Pay for a once-only founding offer with sixty days for the recipient to respond. Both countries must remain independent, present, uncapitulated and not at war with each other. Amber commits one funded slot; refusal or expiry returns that slot but does not refund political or fiscal costs. No military alignment is granted.",
            condition, tag + "_up_send_offer = yes", visible="ac_up_active = yes NOT = { has_country_flag = ac_up_offer_attempted }", weight=5))
        clear = "clr_country_flag = ac_up_offer_pending\nclr_country_flag = " + window + "\n" + guard("country_exists = FCU", "FCU = { clr_country_flag = " + pending + " }")
        returned = ""
        if tag == "AMB":
            returned = guard("has_country_flag = ac_up_offer_slot_committed", "clr_country_flag = ac_up_offer_slot_committed\nadd_to_variable = { ac_up_amber_slots = 1 }\nac_up_bound = yes")
        effects[tag + "_up_close_offer"] = clear + returned
        answerable = f"tag = FCU original_tag = FCU has_country_flag = {pending} country_exists = {tag} {tag} = {{ {valid} = yes has_country_flag = ac_up_offer_pending has_country_flag = {window} }}"
        accept = f"clr_country_flag = {pending}\nset_country_flag = ac_up_{lower}_partner_active\n{tag} = {{\n{clear}\nclr_country_flag = ac_up_offer_slot_committed\nset_country_flag = ac_up_offer_accepted\nset_country_flag = ac_up_partner_active\nac_up_recovery_credit = yes\nadd_opinion_modifier = {{ target = FCU modifier = ac_up_practical_services }}\n}}\nadd_opinion_modifier = {{ target = {tag} modifier = ac_up_practical_services }}\n" + guard("has_country_flag = ac_ucw_started", "add_to_variable = { ac_ucw_recovery = 2 }\nac_ucw_bound = yes")
        effects[tag + "_up_accept_offer"] = guard(answerable, accept)
        refuse = f"clr_country_flag = {pending}\n{tag} = {{ {tag}_up_close_offer = yes set_country_flag = ac_up_offer_refused }}"
        effects[tag + "_up_refuse_offer"] = guard(answerable, refuse)
        # Invalid and late offers close before any subsequent script can pay out.
        expired = guard("has_country_flag = ac_up_offer_pending OR = { NOT = { has_country_flag = " + window + " } " + valid + " = no }", tag + "_up_close_offer = yes\nset_country_flag = ac_up_offer_closed")
        stop = f"clr_country_flag = ac_up_partner_active\nset_country_flag = ac_up_partner_interrupted\nremove_opinion_modifier = {{ target = FCU modifier = ac_up_practical_services }}\n" + guard("country_exists = FCU", f"FCU = {{ clr_country_flag = ac_up_{lower}_partner_active remove_opinion_modifier = {{ target = {tag} modifier = ac_up_practical_services }} }}")
        interrupted = guard("has_country_flag = ac_up_partner_active " + valid + " = no", stop)
        interruption += guard("tag = " + tag, guard("has_country_flag = ac_up_offer_pending", tag + "_up_close_offer = yes\nset_country_flag = ac_up_offer_closed") + guard("has_country_flag = ac_up_partner_active", stop))
        sender_ticks += guard("tag = " + tag, expired + interrupted)
        # FCU clears its own pending marker even if the sender no longer exists.
        recipient_cleanup += guard("has_country_flag = " + pending + " OR = { NOT = { country_exists = " + tag + " } " + tag + " = { " + valid + " = no } " + tag + " = { NOT = { has_country_flag = " + window + " } } }", "clr_country_flag = " + pending + "\n" + guard("country_exists = " + tag, tag + " = { " + tag + "_up_close_offer = yes set_country_flag = ac_up_offer_closed }"))
        recipient_cleanup += guard("has_country_flag = ac_up_" + lower + "_partner_active OR = { NOT = { country_exists = " + tag + " } " + tag + " = { " + valid + " = no } " + tag + " = { NOT = { has_country_flag = ac_up_partner_active } } }", "clr_country_flag = ac_up_" + lower + f"_partner_active\nremove_opinion_modifier = {{ target = {tag} modifier = ac_up_practical_services }}\n" + guard("country_exists = " + tag, tag + " = { clr_country_flag = ac_up_partner_active set_country_flag = ac_up_partner_interrupted remove_opinion_modifier = { target = FCU modifier = ac_up_practical_services } }"))
        ident = "ac_up." + str(101 + offset)
        loc(ident + ".t", cfg["name"] + ": A Bounded Service Offer")
        loc(ident + ".d", cfg["name"] + " has offered a defined civil service, with its own administrative cost already paid. Acceptance records a practical relationship and limited recovery work; it is not a request to create another faction, decide the war or commit unlimited capacity. The offer lapses if either participant becomes ineligible. A refusal leaves the sender with a domestic programme to pursue.")
        loc(ident + ".a", "Accept the bounded service and its receiving obligations.")
        loc(ident + ".b", "Decline; our receiving capacity is committed elsewhere.")
        event = f"id = {ident}\ntitle = {ident}.t\ndesc = {ident}.d\npicture = GFX_report_event_defense_white_paper\nis_triggered_only = yes\n" + block("trigger", answerable)
        event += block("option", f"name = {ident}.a\nai_chance = {{ factor = 65 }}\n{tag}_up_accept_offer = yes")
        event += block("option", f"name = {ident}.b\nai_chance = {{ factor = 35 }}\n{tag}_up_refuse_offer = yes")
        EVENTS.append(block("country_event", event))
    effects["ac_up_diplomacy_tick"] = sender_ticks
    effects["ac_up_interrupt_diplomacy"] = interruption
    effects["ac_up_fcu_cleanup"] = guard("tag = FCU original_tag = FCU", recipient_cleanup)
    emit("common/opinion_modifiers/ac_usean_partners.txt", block("opinion_modifiers", block("ac_up_practical_services", "value = 10")))
    loc("ac_up_practical_services", "Accountable Practical Services")
