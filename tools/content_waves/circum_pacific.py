"""Wave C: the Circum-Pacific War, 2010 (Package 3). Owner only; no focuses.

Osea's and Yuktobania's focus budgets are complete, so this wave delivers the
conflict owner ``ac_cpw`` that the two Pacific squadron stories already read
(``ac_cpw_started``, ``ac_cpw_tainted``, ``ac_cpw_prevented`` and
``ac_cpw_declaration_withheld``), its dated news, two decision events, a few
decisions and the AI weights that keep the historical route reachable.

Source layers
-------------
Official (ACES Chronicle, read 3 November 2026; compiled in
docs/STRANGEREAL_2006_2020_SOURCES.md): the Arkbird Summit (2008 / 08.21) and
every 2010 entry from 09.23 to 12.31, plus the Super Weapons rows for the
Arkbird, the SOLG and Scinfaxi and Hrimfaxi. Named people, squadrons, ships,
places and weapons appear only in event text, exactly as the Chronicle names
them; none becomes a unit, character, leader, state or project.

Mod provenance, read only: ``ac_sp_arkbird`` and its completion flag and ideas,
the Osean and Yuktobanian national continuation records (``ac_snc_*``), the
Yuktobanian Arkbird partnership flag.

Provisional gameplay: every idea value, decision, the fourteen-day declaration
window, the observation rules and the texts of the earned alternatives.

Contract (docs/PACIFIC_NATIONAL_CONTINUATIONS.md): the owner has its own
calendar and declarations; the principal pair and the immediate participant set
are inspected for pre-existing wars; third-party entry permanently moves the
crisis to external observation; factions or guarantees alone never veto the
declaration; there is no scripted white peace; end news follows actual
cessation, never the 31 December anchor or an assumed victory.
"""
from content_waves.framework import Wave, block, guard

P = "ac_cpw"
COUNTRIES = {"OSE": "Osea", "YUK": "Yuktobania"}
WAVE = Wave(
    prefix=P, infix="cpw", label="The Circum-Pacific War", source="tools/content_waves",
    countries={}, eligible="", branches=(), layout={}, openings={}, finals={}, final_ready={},
    themes={"OSE": ("air", "navy"), "YUK": ("submarine", "command")}, extra_tags=("OSE", "YUK"),
)

CALENDAR = "2010.9.21"       # "date > 2010.9.21": the owner's calendar opens on 22 September 2010
ANCHOR = "2010.9.26"         # the declaration, 27 September 2010 (Chronicle, 2010 / 09.27)
LATE_LIMIT = "2011.9.27"     # a first observation a year later never replays the war
SUMMIT = ("2008.8.20", "2009.8.21")

STARTED = "has_global_flag = ac_cpw_started"
ENDED = "has_global_flag = ac_cpw_ended"
TAINTED = "has_global_flag = ac_cpw_tainted"
CLOSED = "has_global_flag = ac_cpw_closed"
ROUTE_SETTLED = f"NOT = {{ {STARTED} }} NOT = {{ has_global_flag = ac_cpw_prevented }} NOT = {{ has_global_flag = ac_cpw_declaration_withheld }} NOT = {{ {CLOSED} }}"

# (name, "date >" anchor, extra condition, body, news event). Each fires once,
# only while the owned war runs untainted. Territorial rows wait for the
# observed Osean foothold; the map itself is never changed.
STAGES = (
    ("eaglin", "2010.9.29", "",
     "OSE = { add_timed_idea = { idea = ac_cpw_ose_carrier_losses days = 90 } }\n" +
     guard("ac_cpw_arkbird_available = yes NOT = { has_global_flag = ac_cpw_arkbird_committed } NOT = { has_global_flag = ac_cpw_arkbird_held_back }",
           "OSE = { country_event = { id = ac_cpw.6 days = 1 } }"), 20),
    ("sand_island", "2010.10.3", "", "remove_ideas = ac_cpw_yuk_submarine_carriers\nadd_ideas = ac_cpw_yuk_submarine_carrier", 21),
    ("akerson_hill", "2010.10.21", "", "", 22),
    ("arkbird_sabotage", "2010.10.24", "has_global_flag = ac_cpw_arkbird_committed",
     "set_global_flag = ac_cpw_arkbird_sabotaged\nOSE = { add_timed_idea = { idea = ac_cpw_ose_arkbird_grounded days = 56 } }", 23),
    ("bastok", "2010.10.31", "ac_cpw_osean_foothold = yes",
     "OSE = { add_timed_idea = { idea = ac_cpw_ose_expeditionary_strain days = 90 } }", 24),
    ("dresdene", "2010.11.1", "has_global_flag = ac_cpw_stage_bastok",
     "OSE = { add_timed_idea = { idea = ac_cpw_ose_dresdene_inquiry days = 60 } }", 25),
    ("bana", "2010.11.3", "", "OSE = { add_timed_idea = { idea = ac_cpw_ose_home_front_alert days = 60 } }", 26),
    ("razgriz_straits", "2010.11.13", "", "remove_ideas = ac_cpw_yuk_submarine_carriers\nremove_ideas = ac_cpw_yuk_submarine_carrier", 27),
    ("november_city", "2010.11.28", "", "OSE = { add_timed_idea = { idea = ac_cpw_ose_home_front_alert days = 60 } }", 28),
    ("cruik", "2010.12.5", "has_global_flag = ac_cpw_stage_bastok ac_cpw_osean_foothold = yes",
     "add_timed_idea = { idea = ac_cpw_yuk_stronghold_lost days = 90 }", 29),
    ("harling", "2010.12.8", "", "OSE = { add_timed_idea = { idea = ac_cpw_ose_president_returns days = 90 } }", 30),
    ("arkbird_lost", "2010.12.18", "has_global_flag = ac_cpw_arkbird_committed",
     "set_global_flag = ac_cpw_arkbird_lost\nremove_ideas = ac_sp_arkbird_joint_operations\n"
     "OSE = { remove_ideas = ac_sp_arkbird_debris_clearing remove_ideas = ac_sp_arkbird_joint_operations "
     "remove_ideas = ac_cpw_ose_arkbird_at_the_front remove_ideas = ac_cpw_ose_arkbird_grounded }", 31),
    ("nikanor", "2010.12.22", "", "add_timed_idea = { idea = ac_cpw_yuk_leadership_question days = 60 }", 32),
    ("ceres", "2010.12.28", "", "", 33),
    ("kestrel", "2010.12.29", "",
     "set_global_flag = ac_cpw_disarmament_appeal\nadd_ideas = ac_cpw_disarmament_appeal\nOSE = { add_ideas = ac_cpw_disarmament_appeal }", 34),
    ("solg", "2010.12.30", "has_global_flag = ac_cpw_stage_kestrel", "", 35),
)

# Every idea the owner adds without a timer; all are removed when the war ends.
WAR_IDEAS = ("ac_cpw_ose_war_footing", "ac_cpw_yuk_war_footing", "ac_cpw_yuk_submarine_carriers",
             "ac_cpw_yuk_submarine_carrier", "ac_cpw_disarmament_appeal", "ac_cpw_ose_arkbird_at_the_front")


def owner():
    effects, triggers, loc, ideas, events = {}, {}, {}, [], []

    def idea(ident, title, description, values):
        loc[ident] = title
        loc[ident + "_desc"] = description
        ideas.append(block(ident, "picture = " + ident + "\nallowed = { always = no }\nallowed_civil_war = { always = no }\nremoval_cost = -1\n" +
                           block("modifier", "\n".join(f"{k} = {v}" for k, v in values.items()))))

    def news(number, picture):
        events.append(block("news_event", f"id = {P}.{number}\ntitle = {P}.{number}.t\ndesc = {P}.{number}.d\npicture = GFX_{picture}\n"
                            "is_triggered_only = yes\nmajor = yes\ntrigger = { always = yes }\n" + block("option", f"name = {P}.{number}.a")))

    # Triggers ---------------------------------------------------------------
    triggers["ac_cpw_principals"] = "country_exists = OSE country_exists = YUK"
    triggers["ac_cpw_war_running"] = f"{STARTED} NOT = {{ {ENDED} }}"
    triggers["ac_cpw_course_open"] = f"ac_cpw_war_running = yes NOT = {{ {TAINTED} }} ac_cpw_principals = yes"
    triggers["ac_cpw_pair_at_war"] = "ac_cpw_principals = yes YUK = { has_war_with = OSE }"
    triggers["ac_cpw_can_declare"] = ("tag = YUK original_tag = YUK has_capitulated = no is_subject = no country_exists = OSE "
                                      f"OSE = {{ has_capitulated = no is_subject = no }} NOT = {{ has_war_with = OSE }} {ROUTE_SETTLED}")
    triggers["ac_cpw_exchange_earned"] = ("ac_cpw_principals = yes OSE = { ac_snc_ose_verification_earned = yes ac_snc_ose_channel_earned = yes } "
                                          "YUK = { ac_snc_yuk_verification_earned = yes ac_snc_yuk_channel_earned = yes }")
    triggers["ac_cpw_mandate_earned"] = "tag = YUK original_tag = YUK ac_snc_yuk_verification_earned = yes"
    triggers["ac_cpw_third_party_present"] = "any_country = { NOT = { tag = OSE } NOT = { tag = YUK } OR = { has_war_with = OSE has_war_with = YUK } }"
    triggers["ac_cpw_osean_foothold"] = "country_exists = OSE OSE = { any_controlled_state = { is_core_of = YUK } }"
    triggers["ac_cpw_arkbird_available"] = "has_global_flag = ac_sp_arkbird_complete NOT = { has_global_flag = ac_cpw_arkbird_lost }"
    triggers["ac_cpw_principal_fallen"] = ("OR = { NOT = { country_exists = OSE } NOT = { country_exists = YUK } has_global_flag = ac_cpw_ose_fallen "
                                           "has_global_flag = ac_cpw_yuk_fallen OSE = { has_capitulated = yes } YUK = { has_capitulated = yes } }")

    # Owner effects ------------------------------------------------------------
    effects["ac_cpw_restore"] = guard("ac_cpw_war_running = yes",
        guard("tag = YUK NOT = { has_idea = ac_cpw_yuk_war_footing }", "add_ideas = ac_cpw_yuk_war_footing") +
        guard("country_exists = OSE OSE = { NOT = { has_idea = ac_cpw_ose_war_footing } }", "OSE = { add_ideas = ac_cpw_ose_war_footing }"))
    effects["ac_cpw_summit_tick"] = (
        guard(f"date > {SUMMIT[0]} NOT = {{ has_global_flag = ac_cpw_summit_held }} NOT = {{ has_global_flag = ac_cpw_summit_skipped }}",
              guard(f"date < {SUMMIT[1]} ac_cpw_principals = yes has_global_flag = ac_sp_arkbird_complete NOT = {{ has_war_with = OSE }}",
                    "set_global_flag = ac_cpw_summit_held\nnews_event = { id = ac_cpw.14 days = 1 }") +
              block("else_if", block("limit", f"date > {SUMMIT[1]}") + "set_global_flag = ac_cpw_summit_skipped")))
    effects["ac_cpw_calendar_tick"] = guard(
        f"date > {CALENDAR} NOT = {{ has_global_flag = ac_cpw_calendar_started }} NOT = {{ {CLOSED} }}",
        guard(f"date < {LATE_LIMIT} ac_cpw_principals = yes", "set_global_flag = ac_cpw_calendar_started") +
        block("else_if", block("limit", f"NOT = {{ date < {LATE_LIMIT} }}") + "set_global_flag = ac_cpw_closed\nset_global_flag = ac_cpw_late_start_skipped") +
        block("else", "set_global_flag = ac_cpw_closed\nset_global_flag = ac_cpw_principal_missing"))
    prelude = ""
    for name, after, number in (("landers", "2010.9.22", 1), ("overflight", "2010.9.23", 2)):
        prelude += guard(f"has_global_flag = ac_cpw_calendar_started date > {after} NOT = {{ has_global_flag = ac_cpw_prelude_{name} }} "
                         f"NOT = {{ {CLOSED} }} ac_cpw_principals = yes NOT = {{ has_war_with = OSE }}",
                         f"set_global_flag = ac_cpw_prelude_{name}\nnews_event = {{ id = ac_cpw.{number} days = 1 }}")
    effects["ac_cpw_prelude_tick"] = prelude
    effects["ac_cpw_observe_existing_war"] = guard(f"ac_cpw_pair_at_war = yes {ROUTE_SETTLED}",
        "set_global_flag = ac_cpw_started\nset_global_flag = ac_cpw_tainted\nset_global_flag = ac_cpw_existing_war_observed\n"
        "news_event = { id = ac_cpw.8 days = 1 }")
    effects["ac_cpw_prevent"] = guard(f"ac_cpw_exchange_earned = yes {ROUTE_SETTLED}",
        "set_global_flag = ac_cpw_prevented\nnews_event = { id = ac_cpw.4 days = 1 }\n"
        "add_timed_idea = { idea = ac_cpw_yuk_exchange_standing days = 365 }\n"
        "OSE = { add_timed_idea = { idea = ac_cpw_ose_exchange_standing days = 365 } }")
    effects["ac_cpw_taint"] = guard(f"ac_cpw_war_running = yes NOT = {{ {TAINTED} }}", "set_global_flag = ac_cpw_tainted")
    effects["ac_cpw_declare"] = guard("ac_cpw_can_declare = yes",
        guard("OR = { has_war = yes OSE = { has_war = yes } }", "set_global_flag = ac_cpw_pre_existing_war") +
        "declare_war_on = { target = OSE type = topple_government }\nset_global_flag = ac_cpw_started\n"
        "clr_country_flag = ac_cpw_declaration_pending\nclr_country_flag = ac_cpw_declaration_window\n"
        "add_ideas = ac_cpw_yuk_war_footing\nadd_ideas = ac_cpw_yuk_submarine_carriers\n"
        "OSE = { add_ideas = ac_cpw_ose_war_footing }\nnews_event = { id = ac_cpw.3 days = 1 }\n" +
        guard("has_global_flag = ac_cpw_pre_existing_war", "ac_cpw_taint = yes\nnews_event = { id = ac_cpw.9 days = 2 }"))
    effects["ac_cpw_withhold"] = guard("ac_cpw_can_declare = yes ac_cpw_mandate_earned = yes",
        "set_global_flag = ac_cpw_declaration_withheld\nclr_country_flag = ac_cpw_declaration_pending\nclr_country_flag = ac_cpw_declaration_window\n"
        "add_timed_idea = { idea = ac_cpw_yuk_mandate_kept days = 365 }\nnews_event = { id = ac_cpw.7 days = 1 }")
    effects["ac_cpw_declaration_tick"] = guard(
        f"has_global_flag = ac_cpw_calendar_started date > {ANCHOR} {ROUTE_SETTLED}",
        guard("ac_cpw_pair_at_war = yes", "ac_cpw_observe_existing_war = yes") +
        block("else_if", block("limit", "ac_cpw_exchange_earned = yes") + "ac_cpw_prevent = yes") +
        block("else_if", block("limit", "ac_cpw_can_declare = yes") +
              guard("NOT = { has_country_flag = ac_cpw_declaration_asked }",
                    "set_country_flag = ac_cpw_declaration_asked\nset_country_flag = ac_cpw_declaration_pending\n"
                    "set_country_flag = { flag = ac_cpw_declaration_window days = 14 }\ncountry_event = { id = ac_cpw.5 days = 1 }") +
              block("else_if", block("limit", "has_country_flag = ac_cpw_declaration_pending NOT = { has_country_flag = ac_cpw_declaration_window }") +
                    "ac_cpw_declare = yes")) +
        block("else", "set_global_flag = ac_cpw_closed\nset_global_flag = ac_cpw_principal_unable"))
    remove_all = "".join(f"remove_ideas = {i}\n" for i in WAR_IDEAS)
    effects["ac_cpw_record_end"] = guard("ac_cpw_war_running = yes",
        "set_global_flag = ac_cpw_ended\n" +
        guard("OR = { NOT = { country_exists = YUK } has_global_flag = ac_cpw_yuk_fallen YUK = { has_capitulated = yes } }",
              "set_global_flag = ac_cpw_outcome_osean_victory\nnews_event = { id = ac_cpw.11 days = 1 }") +
        block("else_if", block("limit", "OR = { NOT = { country_exists = OSE } has_global_flag = ac_cpw_ose_fallen OSE = { has_capitulated = yes } }") +
              "set_global_flag = ac_cpw_outcome_yuktobanian_victory\nnews_event = { id = ac_cpw.12 days = 1 }") +
        block("else_if", block("limit", f"NOT = {{ {TAINTED} }}") +
              "set_global_flag = ac_cpw_outcome_cessation\nset_global_flag = ac_cpw_historical_course\nnews_event = { id = ac_cpw.10 days = 1 }") +
        block("else", "set_global_flag = ac_cpw_outcome_cessation\nnews_event = { id = ac_cpw.13 days = 1 }") +
        guard("country_exists = OSE", "OSE = { " + remove_all.replace("\n", " ") + "}") +
        guard("country_exists = YUK", "YUK = { " + remove_all.replace("\n", " ") + "}"))
    effects["ac_cpw_observation_tick"] = guard("ac_cpw_war_running = yes",
        guard(f"NOT = {{ {TAINTED} }} ac_cpw_third_party_present = yes", "ac_cpw_taint = yes\nnews_event = { id = ac_cpw.9 days = 1 }") +
        guard("OR = { ac_cpw_principal_fallen = yes NOT = { ac_cpw_pair_at_war = yes } }", "ac_cpw_record_end = yes"))
    stages = ""
    for name, after, extra, body, number in STAGES:
        stages += guard(f"ac_cpw_course_open = yes date > {after} NOT = {{ has_global_flag = ac_cpw_stage_{name} }} {extra}".rstrip(),
                        f"set_global_flag = ac_cpw_stage_{name}\n" + body + ("\n" if body else "") + f"news_event = {{ id = ac_cpw.{number} days = 1 }}")
    effects["ac_cpw_stage_tick"] = stages
    effects["ac_cpw_owner_weekly"] = guard("tag = YUK original_tag = YUK",
        "ac_cpw_summit_tick = yes\nac_cpw_calendar_tick = yes\nac_cpw_prelude_tick = yes\nac_cpw_declaration_tick = yes\n"
        "ac_cpw_observation_tick = yes\nac_cpw_stage_tick = yes")
    effects["ac_cpw_owner_weekly_ose"] = guard("tag = OSE original_tag = OSE ac_cpw_war_running = yes NOT = { country_exists = YUK }", "ac_cpw_record_end = yes")
    effects["ac_cpw_interrupt"] = guard("OR = { original_tag = OSE original_tag = YUK } ac_cpw_war_running = yes",
        guard("original_tag = OSE", "set_global_flag = ac_cpw_ose_fallen") + block("else", "set_global_flag = ac_cpw_yuk_fallen") +
        "ac_cpw_record_end = yes")
    effects["ac_cpw_commit_arkbird"] = guard("tag = OSE original_tag = OSE ac_cpw_course_open = yes ac_cpw_arkbird_available = yes NOT = { has_global_flag = ac_cpw_arkbird_committed }",
        "set_global_flag = ac_cpw_arkbird_committed\nadd_ideas = ac_cpw_ose_arkbird_at_the_front\nnews_event = { id = ac_cpw.15 days = 1 }")
    effects["ac_cpw_hold_arkbird"] = guard("tag = OSE original_tag = OSE NOT = { has_global_flag = ac_cpw_arkbird_committed }",
        "set_global_flag = ac_cpw_arkbird_held_back")
    # The decisions' political-power costs are charged by the engine through
    # their `cost`; these effects must not charge them again.
    for tag in COUNTRIES:
        t = tag.lower()
        effects[f"ac_cpw_home_front_{t}"] = guard(f"tag = {tag} original_tag = {tag} ac_cpw_war_running = yes NOT = {{ has_country_flag = {tag}_cpw_home_front_done }}",
            f"set_country_flag = {tag}_cpw_home_front_done\nadd_timed_idea = {{ idea = ac_cpw_{t}_home_front days = 120 }}")
        effects[f"ac_cpw_war_record_{t}"] = guard(f"tag = {tag} original_tag = {tag} {ENDED} NOT = {{ has_country_flag = {tag}_cpw_war_record_done }}",
            f"set_country_flag = {tag}_cpw_war_record_done\nadd_timed_idea = {{ idea = ac_cpw_{t}_war_record days = 180 }}")

    # Ideas (provisional values) ---------------------------------------------------
    idea("ac_cpw_ose_war_footing", "Osea at War", "Yuktobania declared war on Osea on 27 September 2010 (Chronicle, 2010 / 09.27). The federation is on a war footing until the fighting actually ends; this campaign fixes no end date.",
         {"war_support_factor": 0.05, "political_power_gain": -0.1, "consumer_goods_factor": 0.02})
    idea("ac_cpw_yuk_war_footing", "Yuktobania at War", "Yuktobania declared war on Osea on 27 September 2010 (Chronicle, 2010 / 09.27). The union is on a war footing until the fighting actually ends; this campaign fixes no end date.",
         {"war_support_factor": 0.05, "political_power_gain": -0.1, "consumer_goods_factor": 0.02})
    idea("ac_cpw_yuk_submarine_carriers", "Scinfaxi and Hrimfaxi", "Two nuclear-powered submarine carriers are available (Super Weapons, Scinfaxi & Hrimfaxi). Their effect on naval coordination is provisional gameplay.",
         {"naval_coordination": 0.05, "industrial_capacity_dockyard": -0.05})
    idea("ac_cpw_yuk_submarine_carrier", "Hrimfaxi Alone", "Scinfaxi was sunk at Sand Island on 4 October 2010 (Chronicle, 2010 / 10.04). One submarine carrier remains; the value is provisional gameplay.",
         {"naval_coordination": 0.025, "industrial_capacity_dockyard": -0.05})
    idea("ac_cpw_ose_carrier_losses", "The Eaglin Straits Losses", "The carriers Vulture and Buzzard were sunk in the Eaglin Straits on 30 September 2010 (Chronicle, 2010 / 09.30). Naval coordination suffers for ninety days; the value is provisional gameplay.",
         {"naval_coordination": -0.05, "political_power_gain": -0.05})
    idea("ac_cpw_ose_arkbird_at_the_front", "The Arkbird at the Front", "Osea has sent the Arkbird to the front (Chronicle, 2010 / 09.30). The debris-clearing spacecraft now flies military missions; the modifier is provisional gameplay.",
         {"air_mission_efficiency": 0.03, "political_power_gain": -0.03})
    idea("ac_cpw_ose_arkbird_grounded", "The Arkbird Sabotaged", "Smuggled explosives destroyed the Arkbird's engines on 25 October 2010 (Chronicle, 2010 / 10.25). Repairs take eight weeks in this campaign; the duration is provisional gameplay.",
         {"air_mission_efficiency": -0.02, "political_power_gain": -0.03})
    idea("ac_cpw_ose_expeditionary_strain", "The Bastok Expedition", "Osean forces have landed on the Yuktobanian mainland (Chronicle, 2010 / 11.01). Supply across the ocean strains the federation for ninety days; the value is provisional gameplay.",
         {"supply_consumption_factor": 0.05, "political_power_gain": -0.03})
    idea("ac_cpw_ose_dresdene_inquiry", "The Dresdene Inquiry", "Osean aircraft fired on an engineering college in Dresdene (Chronicle, 2010 / 11.02). The inquiry costs political attention for sixty days; the value is provisional gameplay.",
         {"political_power_gain": -0.08, "stability_factor": -0.01})
    idea("ac_cpw_ose_home_front_alert", "Home Front Alert", "Yuktobanian attacks on Osean soil (Chronicle, 2010 / 11.04 and 11.29) keep the federation's home defences on alert for sixty days; the value is provisional gameplay.",
         {"army_core_defence_factor": 0.03, "consumer_goods_factor": 0.01})
    idea("ac_cpw_yuk_stronghold_lost", "Cruik Fortress Lost", "Cruik Fortress, Yuktobania's last defensive stronghold, fell on 6 December 2010 (Chronicle, 2010 / 12.06). Army organisation suffers for ninety days; the value is provisional gameplay.",
         {"army_org_factor": -0.04, "stability_factor": -0.02})
    idea("ac_cpw_ose_president_returns", "The President Returns", "President Harling was rescued from Stier Castle in Belka on 9 December 2010 (Chronicle, 2010 / 12.09). His return steadies the federation for ninety days; the value is provisional gameplay.",
         {"stability_factor": 0.03, "political_power_gain": 0.05})
    idea("ac_cpw_yuk_leadership_question", "The Leadership Question", "Former Prime Minister Nikanor was rescued from imprisonment by the Yuktobanian military on 23 December 2010 (Chronicle, 2010 / 12.23). The union's leadership is in question for sixty days; the value is provisional gameplay.",
         {"political_power_gain": -0.1, "stability_factor": -0.02})
    idea("ac_cpw_disarmament_appeal", "The Joint Appeal to Disarm", "Harling and Nikanor jointly asked their militaries to disarm on 30 December 2010 (Chronicle, 2010 / 12.30). The appeal weighs on both countries' will to fight until the fighting actually ends; the value is provisional gameplay.",
         {"war_support_factor": -0.1, "stability_factor": 0.01})
    idea("ac_cpw_ose_exchange_standing", "The Reciprocal Exchange Holds", "Both governments earned verified contact and open channels before 27 September 2010, and the declaration recorded for that date did not come. This earned alternative is provisional gameplay.",
         {"stability_factor": 0.02, "political_power_gain": -0.03})
    idea("ac_cpw_yuk_exchange_standing", "The Reciprocal Exchange Holds", "Both governments earned verified contact and open channels before 27 September 2010, and the declaration recorded for that date did not come. This earned alternative is provisional gameplay.",
         {"stability_factor": 0.02, "political_power_gain": -0.03})
    idea("ac_cpw_yuk_mandate_kept", "A Declaration Withheld", "Yuktobania's government withheld the declaration of 27 September 2010 under its own mandate. The restraint is honoured at home and questioned by the military for a year; this earned alternative is provisional gameplay.",
         {"stability_factor": 0.02, "army_org_factor": -0.02, "political_power_gain": -0.03})
    idea("ac_cpw_ose_home_front", "Osea: Home Front Mobilised", "The federation has mobilised its home front for 120 days. Industry and defences gain; consumer supply pays. Provisional gameplay.",
         {"industrial_capacity_factory": 0.03, "army_core_defence_factor": 0.03, "consumer_goods_factor": 0.03})
    idea("ac_cpw_yuk_home_front", "Yuktobania: Home Front Mobilised", "The union has mobilised its home front for 120 days. Industry and defences gain; consumer supply pays. Provisional gameplay.",
         {"industrial_capacity_factory": 0.03, "army_core_defence_factor": 0.03, "consumer_goods_factor": 0.03})
    idea("ac_cpw_ose_war_record", "Osea: The War Record", "A public record of the Circum-Pacific War is being compiled for 180 days. It costs political attention and steadies a country that wants to know what happened. Provisional gameplay.",
         {"stability_factor": 0.02, "political_power_gain": -0.05})
    idea("ac_cpw_yuk_war_record", "Yuktobania: The War Record", "A public record of the Circum-Pacific War is being compiled for 180 days. It costs political attention and steadies a country that wants to know what happened. Provisional gameplay.",
         {"stability_factor": 0.02, "political_power_gain": -0.05})

    # Events -----------------------------------------------------------------------
    texts = {
        1: ("Unidentified Aircraft at Cape Landers",
            "Unidentified aircraft have appeared at Cape Landers. Osea's Wardog Squadron engaged them; two of the intruders survived.\n\nThe ACES Chronicle records the incident for 23 September 2010 (2010 / 09.23) and does not identify the aircraft. This campaign asserts nothing beyond the record.",
            "Keep the coast under watch.", "ac_cpw_news_landers"),
        2: ("An SR-71 Over Osea",
            "An unidentified SR-71 has appeared over Osea and was hit by a coastal surface-to-air missile (2010 / 09.24).\n\nThe Chronicle records the overflight and the hit; it names no owner. This campaign names none.",
            "Note the overflight.", "ac_cpw_news_overflight"),
        3: ("Yuktobania Declares War on Osea",
            "Wardog Squadron engaged unidentified aircraft once more. Then Yuktobania declared war on Osea and attacked Port Saint Hewlett. The war the ACES Chronicle calls the Circum-Pacific War has begun (2010 / 09.27).\n\nThe Chronicle gives no reason for the declaration, and this campaign asserts none. The war ends when the fighting actually ends, not on a calendar date.",
            "The Pacific is at war.", "ac_cpw_news_declaration"),
        4: ("The Declaration That Did Not Come",
            "27 September 2010 has passed without a Yuktobanian declaration of war. Both governments earned verified contact and open channels before the date the ACES Chronicle records for the declaration (2010 / 09.27), and the reciprocal exchange closed the route to it.\n\nThis is an earned alternative to the official record and is provisional gameplay. The two countries are not allied, and nothing prevents a later war by other means.",
            "Keep the channels open.", "ac_cpw_news_prevented"),
        7: ("Yuktobania Withholds the Declaration",
            "Yuktobania's government has withheld the declaration of war that the ACES Chronicle records for 27 September 2010 (2010 / 09.27), under the mandate its own field answers and civil policy established.\n\nThis is an earned alternative to the official record and is provisional gameplay. Osea has made no corresponding undertaking; the restraint is Yuktobania's alone.",
            "Record the restraint.", "ac_cpw_news_withheld"),
        8: ("Osea and Yuktobania Already at War",
            "On the date the ACES Chronicle gives for Yuktobania's declaration of war on Osea (2010 / 09.27), the two countries were already fighting one another by other means.\n\nThe Circum-Pacific War owner records that war and observes it from outside. It issues no further dated news of the official course, because the course that produced it did not happen here.",
            "Observe the war as it is.", "ac_cpw_news_observed"),
        9: ("Other Fighting Enters the Pacific War",
            "A third country is now at war with Osea or Yuktobania. The war between the two is no longer the complete explanation of the fighting, and the Circum-Pacific War owner moves to external observation.\n\nThe dated news of the official course stops here. The war's end will still be recorded when the fighting between Osea and Yuktobania actually stops.",
            "Observe the wider war.", "ac_cpw_news_expanded"),
        10: ("The Circum-Pacific War Ends",
             "The fighting between Osea and Yuktobania has stopped. Neither country capitulated.\n\nThe ACES Chronicle records the war's end on 31 December 2010, after the SOLG fell and Razgriz Squadron destroyed it and the former Belkan Grabacr and Ofnir squadrons (2010 / 12.31). This campaign records the end on the day the fighting actually ceased, which is today.",
             "Begin the accounting.", "ac_cpw_news_end"),
        11: ("Yuktobania Capitulates",
             "Yuktobania has capitulated, and the war that began with its declaration on 27 September 2010 (2010 / 09.27) ends in an Osean victory.\n\nThe ACES Chronicle records a different end: a joint appeal to disarm and a ceasefire on 31 December 2010. This outcome is the actual result of the campaign, not the official one.",
             "Record the outcome.", "ac_cpw_news_end"),
        12: ("Osea Capitulates",
             "Osea has capitulated, and the war that began with Yuktobania's declaration on 27 September 2010 (2010 / 09.27) ends in a Yuktobanian victory.\n\nThe ACES Chronicle records a different end: a joint appeal to disarm and a ceasefire on 31 December 2010. This outcome is the actual result of the campaign, not the official one.",
             "Record the outcome.", "ac_cpw_news_end"),
        13: ("The Fighting Between Osea and Yuktobania Stops",
             "The fighting between Osea and Yuktobania has stopped. Other countries had entered the war, so the Circum-Pacific War owner observed it from outside and asserts nothing about how it was fought.\n\nThe ACES Chronicle's course for the war (2010 / 09.27 to 12.31) did not occur here; its end is recorded on the day the fighting actually ceased.",
             "Record the cessation.", "ac_cpw_news_end"),
        14: ("The Arkbird Summit",
             "The Arkbird Summit is held (ACES Chronicle, 2008 / 08.21). The Chronicle records the summit and nothing of its agenda or its result; this campaign adds nothing to the record.\n\nThe Arkbird itself remains the debris-clearing spacecraft completed under the Osean programme.",
             "Note the summit.", "ac_cpw_news_summit"),
        15: ("The Arkbird Goes to the Front",
             "Osea has sent the Arkbird to the front, as the ACES Chronicle records for 30 September 2010 (2010 / 09.30). The spacecraft built to clear Ulysses fragments now flies in a war.\n\nIts later fate follows the Chronicle only while the war keeps its official course.",
             "The Arkbird flies.", "ac_cpw_news_arkbird"),
        20: ("The Eaglin Straits",
             "The submarine Scinfaxi has seen its first use. In the Eaglin Straits the Osean carriers Vulture and Buzzard were sunk (2010 / 09.30).\n\nThe ACES Chronicle also records that Osea sent the Arkbird to the front on this day; in this campaign that depends on whether the Arkbird was ever completed and on the federation's decision.",
             "Count the losses.", "ac_cpw_news_eaglin"),
        21: ("Scinfaxi Sunk at Sand Island",
             "The submarine carrier Scinfaxi has been sunk at Sand Island (2010 / 10.04).\n\nThe Chronicle records the sinking and names no unit; this campaign names none.",
             "One carrier remains.", "ac_cpw_news_sand_island"),
        22: ("The Akerson Hill Incident",
             "The ACES Chronicle records the Akerson Hill Incident for 22 October 2010 (2010 / 10.22). It gives the name only.\n\nThis campaign records the name and nothing else.",
             "Note the record.", "ac_cpw_news_akerson"),
        23: ("The Arkbird's Engines Destroyed",
             "Smuggled explosives have destroyed the Arkbird's engines (2010 / 10.25).\n\nThe Chronicle does not say who smuggled them. The spacecraft is grounded for repair; in this campaign the repair takes eight weeks, which is provisional gameplay.",
             "Begin the repair.", "ac_cpw_news_arkbird"),
        24: ("Osea Lands on the Bastok Peninsula",
             "Osean forces control Yuktobanian territory. The ACES Chronicle records Osea's invasion of the southeastern Yuktobanian mainland on the Bastok Peninsula for 1 November 2010 (2010 / 11.01).\n\nThis campaign reports the landing only because Osean forces actually hold Yuktobanian ground; no territory was moved by script.",
             "Hold the beachhead.", "ac_cpw_news_bastok"),
        25: ("Dresdene",
             "Osean aircraft have fired on an engineering college in Dresdene, killing several people (2010 / 11.02).\n\nThe Chronicle records the attack and the deaths. The federation opens an inquiry; its cost is provisional gameplay.",
             "Open the inquiry.", "ac_cpw_news_dresdene"),
        26: ("Nerve Gas in Bana",
             "Yuktobanian special forces have used nerve gas in Bana and attacked Apito International Airport (2010 / 11.04).\n\nThe Chronicle records both attacks on Osean soil. Home defences are on alert; their effect is provisional gameplay.",
             "Defend the home front.", "ac_cpw_news_bana"),
        27: ("Hrimfaxi Sunk in the Razgriz Straits",
             "The submarine carrier Hrimfaxi has been sunk in the Razgriz Straits (2010 / 11.14).\n\nBoth of Yuktobania's submarine carriers (Super Weapons, Scinfaxi & Hrimfaxi) are now lost.",
             "No carriers remain.", "ac_cpw_news_razgriz_straits"),
        28: ("Attack on the Peace Ceremony",
             "Yuktobanian aircraft have attacked a peace ceremony in November City (2010 / 11.29).\n\nThe Chronicle records the attack and nothing about who ordered it; this campaign asserts nothing more.",
             "Mourn, and keep the alert.", "ac_cpw_news_november_city"),
        29: ("Cruik Fortress Falls",
             "Osean forces have brought down Cruik Fortress, Yuktobania's last defensive stronghold (2010 / 12.06).\n\nThis campaign reports the fall only because Osean forces actually hold Yuktobanian ground; the fortress is not mapped to a state.",
             "The road is open.", "ac_cpw_news_cruik"),
        30: ("President Harling Rescued",
             "President Harling has been rescued from Stier Castle in Belka, and Razgriz Squadron has formed under the president (2010 / 12.09).\n\nThe Chronicle records the rescue, the place and the squadron. It does not say who held the president there, and this campaign does not.",
             "The president returns.", "ac_cpw_news_harling"),
        31: ("The Arkbird Shot Down",
             "The Arkbird, carrying a nuclear weapon, attempted an attack on Okchabursk and was shot down by Razgriz Squadron (2010 / 12.19).\n\nThe debris-clearing spacecraft is lost. The Chronicle does not say who armed it or sent it; this campaign records the loss and nothing else.",
             "The Arkbird is gone.", "ac_cpw_news_arkbird"),
        32: ("Nikanor Rescued",
             "Former Prime Minister Seryozha Viktrovich Nikanor has been rescued from imprisonment by the Yuktobanian military (2010 / 12.23).\n\nThe Chronicle records the rescue and does not say who imprisoned him. The union's leadership is in question; the effect is provisional gameplay.",
             "Who governs Yuktobania?", "ac_cpw_news_nikanor"),
        33: ("The Battle of Ceres Ocean",
             "The ACES Chronicle records the Battle of Ceres Ocean for 29 December 2010 (2010 / 12.29). It gives the name only.\n\nThis campaign records the name and nothing else.",
             "Note the record.", "ac_cpw_news_ceres"),
        34: ("The Joint Appeal to Disarm",
             "The carrier Kestrel has been sunk. Harling and Nikanor have jointly asked their militaries to disarm, and a mixed force is inspecting Gründer Industries in Sudentor, North Osea (2010 / 12.30).\n\nThe appeal weighs on both countries' will to fight. It does not end the war by itself: the fighting ends when it actually stops.",
             "Hear the appeal.", "ac_cpw_news_appeal"),
        35: ("The SOLG Falls",
             "The SOLG has been seen falling. Razgriz Squadron has destroyed the former Belkan Grabacr and Ofnir squadrons and the SOLG itself (2010 / 12.31). The Super Weapons record describes the SOLG as an Osean Cold War orbital railgun, abandoned after the Belkan War and revived by the Gray Men with a V2 warhead.\n\nThe ACES Chronicle ends the war here. This campaign records the end on the day the fighting between Osea and Yuktobania actually stops.",
             "Watch the sky.", "ac_cpw_news_solg"),
    }
    for number, (title, prose, label, picture) in texts.items():
        loc[f"{P}.{number}.t"], loc[f"{P}.{number}.d"], loc[f"{P}.{number}.a"] = title, prose, label
        news(number, picture)
    loc.update({
        "ac_cpw.5.t": "The Declaration of 27 September 2010",
        "ac_cpw.5.d": "Yuktobanian aircraft have been engaged by Osea's Wardog Squadron. The ACES Chronicle records that on this day Yuktobania declared war on Osea and attacked Port Saint Hewlett (2010 / 09.27). It records no reason for the declaration, and this campaign asserts none.\n\nThe government can declare the war the record describes, or withhold the declaration under its own mandate, if that mandate was earned: the field answers settled, a civil floor kept and the command reform or expeditionary assessment completed. Withholding is a provisional alternative to the official record.",
        "ac_cpw.5.a": "Declare war on Osea.",
        "ac_cpw.5.b": "Withhold the declaration under the mandate.",
        "ac_cpw.6.t": "The Arkbird and the Front",
        "ac_cpw.6.d": "The carriers Vulture and Buzzard are lost in the Eaglin Straits. The ACES Chronicle records that Osea sent the Arkbird to the front on this day (2010 / 09.30).\n\nThe federation can send the debris-clearing spacecraft to the front, as the record says, or hold it back on its civil task. Holding it back is a provisional alternative; the Chronicle's later entries about the Arkbird then do not apply.",
        "ac_cpw.6.a": "Send the Arkbird to the front.",
        "ac_cpw.6.b": "Keep the Arkbird on debris duty.",
    })
    events.append(block("country_event", "id = ac_cpw.5\ntitle = ac_cpw.5.t\ndesc = ac_cpw.5.d\npicture = GFX_ac_cpw_event_yuk_declaration\nis_triggered_only = yes\n"
                        "trigger = { tag = YUK original_tag = YUK ac_cpw_can_declare = yes }\n" +
                        block("option", "name = ac_cpw.5.a\nai_chance = { factor = 100 }\nac_cpw_declare = yes") +
                        block("option", "name = ac_cpw.5.b\ntrigger = { ac_cpw_mandate_earned = yes }\nai_chance = { factor = 0 }\nac_cpw_withhold = yes")))
    events.append(block("country_event", "id = ac_cpw.6\ntitle = ac_cpw.6.t\ndesc = ac_cpw.6.d\npicture = GFX_ac_cpw_event_ose_arkbird\nis_triggered_only = yes\n"
                        "trigger = { tag = OSE original_tag = OSE ac_cpw_course_open = yes ac_cpw_arkbird_available = yes NOT = { has_global_flag = ac_cpw_arkbird_committed } }\n" +
                        block("option", "name = ac_cpw.6.a\nai_chance = { factor = 100 }\nac_cpw_commit_arkbird = yes") +
                        block("option", "name = ac_cpw.6.b\nai_chance = { factor = 0 }\nac_cpw_hold_arkbird = yes")))

    # Decisions ----------------------------------------------------------------------
    categories, decisions = [], {}
    for tag, country in COUNTRIES.items():
        t = tag.lower()
        category = f"ac_cpw_{t}_crisis"
        loc[category] = country + ": The Circum-Pacific War"
        loc[category + "_desc"] = "[ac_cpw_status_text]\n\nThe war owner follows the ACES Chronicle's 2010 entries as reference anchors. It changes no territory, creates no unit and ends the war only when the fighting actually stops."
        categories.append(block(category, f"icon = GFX_ac_cpw_category_{t}\nallowed = {{ tag = {tag} original_tag = {tag} }}\nvisible = {{ has_global_flag = ac_cpw_calendar_started }}"))
        rows = []
        for key, title, description, visible, available, cost in (
                ("home_front", "Mobilise the Home Front", "Mobilise industry and home defences for 120 days while the war runs. Consumer supply pays for it. Once per war; provisional gameplay.",
                 "ac_cpw_war_running = yes", f"ac_cpw_war_running = yes has_capitulated = no NOT = {{ has_country_flag = {tag}_cpw_home_front_done }}", 50),
                ("war_record", "Compile the War Record", "Compile a public record of the Circum-Pacific War over 180 days. It costs political attention and steadies the country. Once; provisional gameplay.",
                 f"{ENDED}", f"{ENDED} has_capitulated = no NOT = {{ has_country_flag = {tag}_cpw_war_record_done }}", 25)):
            ident = f"{tag}_cpw_{key}"
            loc[ident], loc[ident + "_desc"] = title, description
            rows.append(block(ident, f"icon = ac_cpw_{ident}\nallowed = {{ tag = {tag} original_tag = {tag} }}\nvisible = {{ {visible} }}\navailable = {{ {available} }}\n"
                              f"cost = {cost}\nfire_only_once = yes\n" + block("complete_effect", f"ac_cpw_{key}_{t} = yes") + "ai_will_do = { base = 3 }\n"))
        decisions[category] = rows

    # Defined texts and readable flags ---------------------------------------------------
    status = (("has_global_flag = ac_cpw_outcome_osean_victory", "Ended: Yuktobania capitulated. The official ceasefire of 31 December 2010 did not occur."),
              ("has_global_flag = ac_cpw_outcome_yuktobanian_victory", "Ended: Osea capitulated. The official ceasefire of 31 December 2010 did not occur."),
              ("has_global_flag = ac_cpw_historical_course", "Ended: the fighting stopped without capitulation, after the official course of 27 September to 31 December 2010."),
              ("has_global_flag = ac_cpw_ended", "Ended: the fighting stopped while the owner observed a wider war from outside."),
              ("has_global_flag = ac_cpw_tainted", "Running under external observation: other fighting entered the war, and the official course is no longer asserted."),
              ("has_global_flag = ac_cpw_started", "Running on the official course since 27 September 2010 (Chronicle, 2010 / 09.27)."),
              ("has_global_flag = ac_cpw_prevented", "Prevented: the reciprocal exchange closed the declaration route (earned alternative, provisional gameplay)."),
              ("has_global_flag = ac_cpw_declaration_withheld", "Withheld: Yuktobania kept its mandate and did not declare (earned alternative, provisional gameplay)."),
              ("has_global_flag = ac_cpw_closed", "Closed: the principal pair could not fight the recorded war, or the record's dates had passed."),
              (None, "Pending: the ACES Chronicle records Yuktobania's declaration of war on Osea for 27 September 2010."))
    entries = ""
    for n, (flag, value) in enumerate(status):
        loc[f"ac_cpw_status_{n}"] = value
        entries += block("text", (f"trigger = {{ has_global_flag = {flag.split(' = ')[1]} }}\n" if flag else "") + f"localization_key = ac_cpw_status_{n}")
    custom = block("defined_text", "name = ac_cpw_status_text\n" + entries)
    loc.update({
        "ac_cpw_started": "The Circum-Pacific War has begun",
        "ac_cpw_tainted": "The Circum-Pacific War is under external observation",
        "ac_cpw_prevented": "The 2010 declaration was prevented by the reciprocal exchange",
        "ac_cpw_declaration_withheld": "Yuktobania withheld the 2010 declaration",
        "ac_cpw_ended": "The Circum-Pacific War has ended",
        "ac_cpw_closed": "The Circum-Pacific War owner is closed",
        "ac_cpw_calendar_started": "The Circum-Pacific War calendar is open",
        "ac_cpw_historical_course": "The Circum-Pacific War followed its official course",
        "ac_cpw_outcome_cessation": "The fighting between Osea and Yuktobania stopped without capitulation",
        "ac_cpw_outcome_osean_victory": "Yuktobania capitulated",
        "ac_cpw_outcome_yuktobanian_victory": "Osea capitulated",
        "ac_cpw_pre_existing_war": "A principal was already at war when the declaration came",
        "ac_cpw_existing_war_observed": "Osea and Yuktobania were already at war on 27 September 2010",
        "ac_cpw_late_start_skipped": "The 2010 dates had passed before this content first loaded",
        "ac_cpw_principal_missing": "Osea or Yuktobania did not exist when the calendar opened",
        "ac_cpw_principal_unable": "Osea or Yuktobania could not fight the recorded war",
        "ac_cpw_arkbird_committed": "The Arkbird was sent to the front",
        "ac_cpw_arkbird_held_back": "The Arkbird was kept on debris duty (provisional alternative)",
        "ac_cpw_arkbird_sabotaged": "The Arkbird's engines were destroyed",
        "ac_cpw_arkbird_lost": "The Arkbird was shot down",
        "ac_cpw_disarmament_appeal": "Harling and Nikanor have asked their militaries to disarm",
        "ac_cpw_summit_held": "The Arkbird Summit was held",
        "ac_cpw_summit_skipped": "The Arkbird Summit date passed without a completed Arkbird",
        "ac_cpw_declaration_asked": "The Yuktobanian government has been asked about the declaration",
        "ac_cpw_declaration_pending": "The Yuktobanian declaration is pending",
        "ac_cpw_declaration_window": "The declaration window is open",
        "ac_cpw_ose_fallen": "Osea has fallen during the Circum-Pacific War",
        "ac_cpw_yuk_fallen": "Yuktobania has fallen during the Circum-Pacific War",
        "ac_cpw_principals": "Osea and Yuktobania both exist",
        "ac_cpw_war_running": "The Circum-Pacific War is running",
        "ac_cpw_course_open": "The Circum-Pacific War follows its official course",
        "ac_cpw_pair_at_war": "Osea and Yuktobania are at war",
        "ac_cpw_can_declare": "Yuktobania can declare the recorded war",
        "ac_cpw_exchange_earned": "Both governments earned verified contact and open channels",
        "ac_cpw_mandate_earned": "Yuktobania's verification mandate is earned",
        "ac_cpw_third_party_present": "A third country is at war with Osea or Yuktobania",
        "ac_cpw_osean_foothold": "Osean forces control Yuktobanian territory",
        "ac_cpw_arkbird_available": "The Arkbird is complete and not lost",
        "ac_cpw_principal_fallen": "A principal has capitulated or fallen",
    })
    for name, _, _, _, number in STAGES:
        loc[f"ac_cpw_stage_{name}"] = "Circum-Pacific War stage: " + loc[f"{P}.{number}.t"]
    for name in ("landers", "overflight"):
        loc[f"ac_cpw_prelude_{name}"] = "Circum-Pacific War prelude: " + loc[f"{P}.{1 if name == 'landers' else 2}.t"]

    hooks = (block("on_startup", block("effect", "if = { limit = { country_exists = YUK } YUK = { ac_cpw_restore = yes } }")) +
             block("on_weekly_YUK", block("effect", "ac_cpw_owner_weekly = yes")) +
             block("on_weekly_OSE", block("effect", "ac_cpw_owner_weekly_ose = yes")) +
             block("on_annex", block("effect", "FROM = { ac_cpw_interrupt = yes }")) +
             block("on_capitulation_immediate", block("effect", "ac_cpw_interrupt = yes")) +
             block("on_subject_annexed", block("effect", "ac_cpw_interrupt = yes")))
    ai = "\n".join((
        block("ac_cpw_yuk_tension", "allowed = { original_tag = YUK }\n" +
              block("enable", f"has_global_flag = ac_cpw_calendar_started {ROUTE_SETTLED}") +
              "abort_when_not_enabled = yes\nai_strategy = { type = antagonize id = OSE value = 60 }"),
        block("ac_cpw_yuk_war", "allowed = { original_tag = YUK }\n" + block("enable", "ac_cpw_war_running = yes") +
              "abort_when_not_enabled = yes\nai_strategy = { type = conquer id = OSE value = 150 }"),
        block("ac_cpw_ose_war", "allowed = { original_tag = OSE }\n" + block("enable", "ac_cpw_war_running = yes") +
              "abort_when_not_enabled = yes\nai_strategy = { type = conquer id = YUK value = 120 }"),
    ))
    return dict(effects=effects, triggers=triggers, loc=loc, ideas=ideas, events=events, custom=custom,
                categories=categories, decisions=decisions, hooks=hooks, ai_strategy=ai)


# Registry declarations ------------------------------------------------------
KEY = "C"
NAME = "circum_pacific"
LEDGER = "docs/CONTENT_WAVE_C.md"
SOURCES = {"official": ["Chronicle 2008 / 08.21: the Arkbird Summit",
                        "Chronicle 2010 / 09.23 to 12.31: the Circum-Pacific War",
                        "Super Weapons: Arkbird; SOLG; Scinfaxi & Hrimfaxi"],
           "mod_provenance": "ac_sp_arkbird state and the Osean/Yuktobanian national continuation records, read only",
           "provisional_gameplay": "Every idea value, decision, the declaration window, the observation rules and the earned alternatives' texts"}
NEWS_ART = (("ac_cpw_news_landers", ("air", "radar"), "Unidentified Aircraft at Cape Landers", "OSE"),
            ("ac_cpw_news_overflight", ("radar", "missile"), "An SR-71 Over Osea", "OSE"),
            ("ac_cpw_news_declaration", ("command", "navy"), "Yuktobania Declares War on Osea", "YUK"),
            ("ac_cpw_news_prevented", ("diplomacy", "peace"), "The Declaration That Did Not Come", "YUK"),
            ("ac_cpw_news_withheld", ("assembly", "document"), "Yuktobania Withholds the Declaration", "YUK"),
            ("ac_cpw_news_observed", ("telescope", "navy"), "Osea and Yuktobania Already at War", "OSE"),
            ("ac_cpw_news_expanded", ("telescope", "command"), "Other Fighting Enters the Pacific War", "OSE"),
            ("ac_cpw_news_end", ("peace", "navy"), "The Circum-Pacific War Ends", "OSE"),
            ("ac_cpw_news_summit", ("satellite", "diplomacy"), "The Arkbird Summit", "OSE"),
            ("ac_cpw_news_arkbird", ("satellite", "air"), "The Arkbird", "OSE"),
            ("ac_cpw_news_eaglin", ("carrier", "submarine"), "The Eaglin Straits", "OSE"),
            ("ac_cpw_news_sand_island", ("submarine", "navy"), "Scinfaxi Sunk at Sand Island", "YUK"),
            ("ac_cpw_news_akerson", ("document", "security"), "The Akerson Hill Incident", "OSE"),
            ("ac_cpw_news_bastok", ("logistics", "navy"), "Osea Lands on the Bastok Peninsula", "OSE"),
            ("ac_cpw_news_dresdene", ("civil", "air"), "Dresdene", "YUK"),
            ("ac_cpw_news_bana", ("medical", "runway"), "Nerve Gas in Bana", "OSE"),
            ("ac_cpw_news_razgriz_straits", ("submarine", "meteor"), "Hrimfaxi Sunk in the Razgriz Straits", "YUK"),
            ("ac_cpw_news_november_city", ("peace", "air"), "Attack on the Peace Ceremony", "OSE"),
            ("ac_cpw_news_cruik", ("gate", "command"), "Cruik Fortress Falls", "YUK"),
            ("ac_cpw_news_harling", ("assembly", "air"), "President Harling Rescued", "OSE"),
            ("ac_cpw_news_nikanor", ("assembly", "security"), "Nikanor Rescued", "YUK"),
            ("ac_cpw_news_ceres", ("navy", "telescope"), "The Battle of Ceres Ocean", "OSE"),
            ("ac_cpw_news_appeal", ("peace", "assembly"), "The Joint Appeal to Disarm", "OSE"),
            ("ac_cpw_news_solg", ("satellite", "meteor"), "The SOLG Falls", "OSE"))
EVENT_ART = (("ac_cpw_event_yuk_declaration", ("command", "navy"), "The Declaration of 27 September 2010", "YUK"),
             ("ac_cpw_event_ose_arkbird", ("satellite", "carrier"), "The Arkbird and the Front", "OSE"))
OWNER_ART = {
    "ac_cpw_ose_war_footing": ("command", "navy", "OSE"), "ac_cpw_yuk_war_footing": ("command", "submarine", "YUK"),
    "ac_cpw_yuk_submarine_carriers": ("submarine", "carrier", "YUK"), "ac_cpw_yuk_submarine_carrier": ("submarine", "navy", "YUK"),
    "ac_cpw_ose_carrier_losses": ("carrier", "navy", "OSE"), "ac_cpw_ose_arkbird_at_the_front": ("satellite", "air", "OSE"),
    "ac_cpw_ose_arkbird_grounded": ("satellite", "tools", "OSE"), "ac_cpw_ose_expeditionary_strain": ("logistics", "navy", "OSE"),
    "ac_cpw_ose_dresdene_inquiry": ("scales", "document", "OSE"), "ac_cpw_ose_home_front_alert": ("security", "radar", "OSE"),
    "ac_cpw_yuk_stronghold_lost": ("gate", "security", "YUK"), "ac_cpw_ose_president_returns": ("assembly", "civil", "OSE"),
    "ac_cpw_yuk_leadership_question": ("assembly", "ballot", "YUK"), "ac_cpw_disarmament_appeal": ("peace", "assembly", "OSE"),
    "ac_cpw_ose_exchange_standing": ("diplomacy", "communications", "OSE"), "ac_cpw_yuk_exchange_standing": ("diplomacy", "communications", "YUK"),
    "ac_cpw_yuk_mandate_kept": ("document", "peace", "YUK"), "ac_cpw_ose_home_front": ("industry", "security", "OSE"),
    "ac_cpw_yuk_home_front": ("industry", "security", "YUK"), "ac_cpw_ose_war_record": ("document", "scales", "OSE"),
    "ac_cpw_yuk_war_record": ("document", "scales", "YUK"),
}
