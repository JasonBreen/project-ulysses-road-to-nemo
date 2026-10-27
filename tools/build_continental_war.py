"""Deterministic authoring source for the Usean Continental War arc (Python 3.9+).

Run without arguments to regenerate the ac_ucw files and the Erusea/Central
Usea focus trees. --check is read-only. Dated claims are cited in
docs/USEAN_CONTINENTAL_WAR.md; pressure indices, coefficients, branch choices,
the war-start window, stage timings and Stonehenge's map state are
provisional gameplay.
"""
import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod/2985041246"
OUTPUT = {}
LOC = {}
EFFECTS = []
TRIGGERS = []
EVENTS = ["add_namespace = ac_ucw"]
DECISIONS = {"ac_ucw_fallout": [], "ac_ucw_war": [], "ac_playtest": []}
TREES = {"ERU": [], "FCU": []}
IDEAS = []
TAGS = ("ERU", "FCU", "SNS", "AMB", "UGE", "DEL", "NPT")
ENEMIES = ("FCU", "SNS", "AMB", "UGE", "DEL", "NPT")
# Provisional gameplay: the Chronicle places Stonehenge in a desert region of
# San Salvacion but names no state. This is the only place the ID appears.
STONEHENGE_STATE = 310
OUTCOMES = ("isaf_victory", "erusean_victory", "stalemate")


def loc(key, text):
    assert key not in LOC, key
    LOC[key] = text


def block(key, body):
    return key + " = {\n" + "\n".join(("\t" + line).rstrip() for line in body.splitlines()) + "\n}\n"


def changes(grievance=0, pressure=0, recovery=0):
    return "\n".join("add_to_variable = { ac_ucw_%s = %s }" % (name, value)
                     for name, value in (("grievance", grievance), ("pressure", pressure), ("recovery", recovery)) if value)


def effect(name, body):
    EFFECTS.append(block(name, body))


def trigger(name, body):
    TRIGGERS.append(block(name, body))


def once(flag, body, condition="ac_ucw_active = yes"):
    return block("if", "limit = { %s NOT = { has_country_flag = %s } }\nset_country_flag = %s\n%s\nac_ucw_bound = yes" % (condition, flag, flag, body))


def gonce(flag, body, condition="always = yes"):
    return block("if", "limit = { %s NOT = { has_global_flag = %s } }\nset_global_flag = %s\n%s" % (condition, flag, flag, body))


def event(number, title, desc, options, trigger_text="always = yes", picture="GFX_report_event_treaty_2", news=False):
    key = "ac_ucw.%d" % number
    loc(key + ".t", title)
    # Long-form briefings live in TEXT; the inline desc is the fallback summary.
    loc(key + ".d", TEXT.get(number, desc))
    body = "id = %s\ntitle = %s.t\ndesc = %s.d\npicture = %s\nis_triggered_only = yes\n" % (key, key, key, picture)
    if news:
        body += "major = yes\n"
    body += "trigger = { %s }\n" % trigger_text
    for index, (label, reward, condition, weight) in enumerate(options):
        option_key = key + "." + chr(97 + index)
        loc(option_key, label)
        body += block("option", "name = %s\n%sai_chance = { factor = %s }\n%s" % (
            option_key, "trigger = { %s }\n" % condition if condition else "", weight, reward))
    EVENTS.append(block("news_event" if news else "country_event", body))


def brief(number, title, desc, picture="GFX_report_event_blk_army_attack"):
    event(number, title, desc, [("Noted.", "", "", 100)], picture=picture, news=True)


def focus(tag, suffix, title, desc, x, y, icon, prerequisite=(), available="", reward="", excludes=(), cost=5, ai=20):
    ident = "%s_ucw_%s" % (tag, suffix)
    loc(ident, title)
    loc(ident + "_desc", desc)
    body = "id = %s\nicon = %s\nx = %s\ny = %s\ncost = %s\nai_will_do = { factor = %s }\n" % (ident, icon, x, y, cost, ai)
    if prerequisite:
        body += "prerequisite = { %s }\n" % " ".join("focus = %s_ucw_%s" % (tag, item) for item in prerequisite)
    if excludes:
        body += "mutually_exclusive = { %s }\n" % " ".join("focus = %s_ucw_%s" % (tag, item) for item in excludes)
    body += "available = { original_tag = %s ac_ucw_active = yes %s }\ncancel_if_invalid = yes\ncontinue_if_invalid = no\n" % (tag, available)
    body += block("completion_reward", once(ident + "_done", reward))
    body += "search_filters = { }\n"
    TREES[tag].append(block("focus", body))
    return ident


def decision(category, ident, title, desc, available, reward, cost=50, visible="", cooldown=0, single=True, ai=1,
             allowed="ac_ucw_participant = yes", active="ac_ucw_active = yes"):
    loc(ident, title)
    loc(ident + "_desc", desc)
    body = "allowed = { %s }\nvisible = { %s }\navailable = { %s %s }\ncost = %s\nai_will_do = { base = %s }\n" % (allowed, visible, active, available, cost, ai)
    body += "fire_only_once = %s\n" % ("yes" if single else "no")
    if cooldown:
        body += "days_re_enable = %s\n" % cooldown
    guard = active + " " + available
    if single:
        guard += " NOT = { has_country_flag = " + ident + "_taken }"
        reward = "set_country_flag = " + ident + "_taken\n" + reward
    body += block("complete_effect", block("if", "limit = { " + guard + " }\n" + reward + "\nac_ucw_bound = yes"))
    DECISIONS[category].append(block(ident, body))


def idea(ident, title, desc, picture, modifiers):
    loc(ident, title)
    loc(ident + "_desc", desc)
    IDEAS.append(block(ident, "picture = %s\nallowed = { always = no }\nallowed_civil_war = { always = no }\nremoval_cost = -1\n%s" % (picture, block("modifier", modifiers))))


def scoped(tag, body):
    """Run body in another participant's scope only while it exists."""
    return block("if", "limit = { country_exists = %s }\n%s" % (tag, block(tag, body)))


def build_core():
    trigger("ac_ucw_participant", "OR = { " + " ".join("original_tag = " + tag for tag in TAGS) + " }")
    trigger("ac_ucw_active", "has_country_flag = ac_ucw_started\nhas_capitulated = no")
    trigger("ac_ucw_controls_stonehenge", "%d = { is_controlled_by = ROOT }" % STONEHENGE_STATE)
    trigger("ac_ucw_stonehenge_held_by_erusea", "%d = { is_controlled_by = ERU }" % STONEHENGE_STATE)
    trigger("ac_ucw_war_over", "OR = { " + " ".join("has_global_flag = ac_ucw_outcome_" + o for o in OUTCOMES) + " }")
    trigger("ac_ucw_war_running", "has_global_flag = ac_ucw_war_started\nac_ucw_war_over = no")
    trigger("ac_ucw_can_start_war", """original_tag = ERU
has_global_flag = ac_ucw_calendar_started
NOT = { has_global_flag = ac_ucw_war_started }
NOT = { has_global_flag = ac_ucw_war_averted }
has_capitulated = no
country_exists = SNS
country_exists = FCU
NOT = { has_war_with = SNS }""")
    trigger("ac_ucw_playtest_shortcuts_on", "has_game_rule = { rule = ac_playtest_shortcuts option = enabled }")
    effect("ac_ucw_bound", "\n".join(
        "if = { limit = { has_variable = ac_ucw_%s } clamp_variable = { var = ac_ucw_%s min = 0 max = 100 } }" % (name, name)
        for name in ("grievance", "pressure", "recovery")))
    loc("ac_ucw_grievance", "Erusean grievance")
    loc("ac_ucw_pressure", "Refugee pressure")
    loc("ac_ucw_recovery", "Fallout recovery")
    # World calendar: one start for everybody, after The Peace We Inherit's
    # end-of-1999 assessment (ac_pwi.72), or at once through the playtest rule.
    late = "\n".join("if = { limit = { date > %s } set_global_flag = %s_done }" % (when, flag) for flag, when, *_ in BRIEFS)
    effect("ac_ucw_world_start", gonce("ac_ucw_calendar_started", """# Chronicle 1998/06.19: Stonehenge is complete before the arc begins,
# unless the Strangereal special project already recorded it.
if = { limit = { OR = { has_global_flag = ac_sp_stonehenge_complete date > 1998.6.18 } } set_global_flag = ac_ucw_stonehenge_operational }
# A save first loaded after a milestone records it as past and never replays it.
if = { limit = { date > 2000.4.21 } set_global_flag = ac_ucw_refugee_closure_done }
%s
if = { limit = { date > 2004.12.31 } set_global_flag = ac_ucw_late_calendar }""" % late,
        "OR = { date > 1999.11.30 has_global_flag = ac_ucw_playtest_forced }"))
    effect("ac_ucw_country_start", once("ac_ucw_started", """set_variable = { ac_ucw_pressure = 40 }
set_variable = { ac_ucw_recovery = 45 }
if = { limit = { has_country_flag = ac_pwi_relief_strained } add_to_variable = { ac_ucw_pressure = 15 } add_to_variable = { ac_ucw_recovery = -10 } }
if = { limit = { has_country_flag = ac_pwi_relief_resilient } add_to_variable = { ac_ucw_pressure = -15 } add_to_variable = { ac_ucw_recovery = 10 } }
if = { limit = { original_tag = ERU } set_variable = { ac_ucw_grievance = 45 } load_focus_tree = { tree = ac_ucw_eru_tree keep_completed = yes } }
if = { limit = { original_tag = FCU } set_variable = { ac_ucw_stage_weeks = 0 } load_focus_tree = { tree = ac_ucw_fcu_tree keep_completed = yes } }
country_event = { id = ac_ucw.1 days = 1 }""", "ac_ucw_participant = yes has_global_flag = ac_ucw_calendar_started has_capitulated = no"))
    loc("ac_ucw_fallout", "After Ulysses: Usea")
    loc("ac_ucw_fallout_desc", "USEAN BRIEFING\nRefugee pressure: [?ac_ucw_pressure|.0]/100. Fallout recovery: [?ac_ucw_recovery|.0]/100.\nThe official chronology records Erusea closing its border to refugees on 21 April 2000 and the invasion of San Salvacion in the summer of 2003. The indices, choices and any averted or earlier war are provisional gameplay.")
    loc("ac_ucw_war", "The Usean Continental War")
    loc("ac_ucw_war_desc", "WAR BRIEFING\nThe stage chain follows the official chronology: ISAF forms on 22 August 2003, falls back to Los Canas, moves its headquarters to North Point, lands on the continent and destroys Stonehenge. Each stage fires once. Borders change only through the war itself; stage timings are provisional gameplay.")
    OUTPUT["common/decisions/categories/ac_ucw.txt"] = (
        block("ac_ucw_fallout", "priority = 60\nvisible_when_empty = yes\nallowed = { ac_ucw_participant = yes }\nvisible = { has_country_flag = ac_ucw_started NOT = { has_global_flag = ac_ucw_war_started } }")
        + block("ac_ucw_war", "priority = 61\nvisible_when_empty = yes\nallowed = { OR = { original_tag = ERU original_tag = FCU } }\nvisible = { has_country_flag = ac_ucw_started has_global_flag = ac_ucw_war_started }")
        + block("ac_playtest", "priority = 200\nvisible_when_empty = yes\nallowed = { always = yes }\nvisible = { ac_ucw_playtest_shortcuts_on = yes }"))
    event(1, "After Ulysses: the Usean brief", "Ulysses passed Earth's Roche limit in July 1999. Usea now carries the weight of the fallout: displaced families, damaged harvests and governments arguing over who should carry the cost. [Root.GetLeader]'s cabinet must decide how to manage refugee pressure and recovery. These indices are provisional gameplay, not a record of impact sites in our provinces.", [("Open the Usean brief.", "", "", 100)], picture="GFX_report_event_bad_news_1")


def build_fallout():
    effect("ac_ucw_fallout_tick", """if = {
    limit = { original_tag = ERU date > 2000.4.20 NOT = { has_global_flag = ac_ucw_refugee_closure_done } }
    set_global_flag = ac_ucw_refugee_closure_done
    country_event = { id = ac_ucw.10 days = 1 }
}""")
    event(10, "Erusea and the refugee columns", "The official chronology records that Erusea stopped taking in refugees on 21 April 2000. The ministries report that camps along the frontier are full and that every week brings new arrivals. Closing the border is the recorded course. Keeping it open under quotas is a provisional alternative and would cost recovery.", [
        ("Close the border.", changes(5, -10) + "\nset_global_flag = ac_ucw_border_closed\nnews_event = { id = ac_ucw.12 days = 1 }\n" + scoped("FCU", "country_event = { id = ac_ucw.11 days = 2 }"), "", 90),
        ("Keep the border open under quotas.", changes(-10, 10, -5) + "\nset_global_flag = ac_ucw_border_open", "", 10)], picture="GFX_report_event_protest_1")
    event(11, "Refugees turn to Central Usea", "With the Erusean border closed, displaced families are moving toward Central Usea and its allies. The Federation can absorb the cost directly or press its treaty partners to share it.", [
        ("Open relief camps.", changes(0, 10, -3) + "\nadd_political_power = -25\nadd_timed_idea = { idea = ac_ucw_refugee_relief days = 365 }", "", 60),
        ("Ask the treaty partners to share the burden.", changes(0, 5) + "\nadd_stability = -0.02", "", 40)], picture="GFX_report_event_protests_2")
    brief(12, "Erusea closes its border", "The official chronology records that Erusea stopped taking in refugees on 21 April 2000. Columns of displaced families have turned away from the frontier, and the governments of Usea are left to argue over who will take them in.", picture="GFX_report_event_bad_news_2")
    event(13, "Central Usea offers mediation", "Central Usea proposes talks on refugees, reconstruction credit and the status of Stonehenge. Accepting lowers tension with our neighbours. Refusing tells the nation that its grievances will not be negotiated away. Provisional gameplay.", [
        ("Accept the talks.", changes(-10) + "\nadd_opinion_modifier = { target = FCU modifier = ac_ucw_mediation }\n" + scoped("FCU", "add_opinion_modifier = { target = ERU modifier = ac_ucw_mediation }\ncountry_event = { id = ac_ucw.14 days = 1 }"), "", 50),
        ("Refuse.", changes(5) + "\n" + scoped("FCU", "country_event = { id = ac_ucw.15 days = 1 }"), "", 50)], picture="GFX_report_event_treaty_1")
    event(14, "Erusea accepts the talks", "Erusea has agreed to talks. Grievance in Farbanti has eased for now; it has not disappeared.", [("Record the agreement.", "", "", 100)])
    event(15, "Erusea refuses the talks", "Erusea has refused mediation. Its government says that Usea's richer states should carry the cost of the fallout themselves.", [("Note the refusal.", "", "", 100)], picture="GFX_report_event_bad_news_1")
    peace = "NOT = { has_global_flag = ac_ucw_war_started } NOT = { has_global_flag = ac_ucw_war_averted }"
    eru = "original_tag = ERU"
    fcu = "original_tag = FCU"
    decision("ac_ucw_fallout", "ac_ucw_eru_blame_the_fcu", "Blame the Federation", "Tell the nation that Central Usea profits from Erusea's suffering. Grievance +10, war support +2 percentage points. Once every 120 days. Provisional gameplay.", peace, changes(10) + "\nadd_war_support = 0.02", cost=25, visible=eru, cooldown=120, single=False, ai=1)
    decision("ac_ucw_fallout", "ac_ucw_eru_public_works", "Fund fallout public works", "Spend political capital on reconstruction: recovery +8, grievance -5. Once every 180 days. If the fiscal prototype is enabled, it also requests its reconstruction policy.", peace + " check_variable = { ac_ucw_recovery < 90 }", changes(-5, 0, 8) + "\nif = { limit = { ac_econ_ready = yes } ac_econ_set_reconstruction = yes }", visible=eru, cooldown=180, single=False, ai=1)
    decision("ac_ucw_fallout", "ac_ucw_eru_refugee_accord", "Reopen a refugee quota", "Accept a limited refugee quota under a regional accord: grievance -12, refugee pressure -10. Once every 180 days. Provisional gameplay.", peace, changes(-12, -10), cost=75, visible=eru, cooldown=180, single=False, ai=0)
    decision("ac_ucw_fallout", "ac_ucw_eru_war_plan", "Draw up the San Salvacion plan", "Requires grievance of at least 70 and mobilized reserves. Allows an invasion of San Salvacion before the summer of 2003. Provisional gameplay: the official chronology records only the 2003 invasion.", peace + " check_variable = { ac_ucw_grievance > 69 } has_country_flag = ac_ucw_eru_mobilized", "set_country_flag = ac_ucw_war_plan_ready", visible=eru, ai=0)
    decision("ac_ucw_fallout", "ac_ucw_eru_invade_san_salvacion", "Invade San Salvacion", "Declare war on San Salvacion and seize Stonehenge. The official chronology dates the invasion to the summer of 2003. Earlier, it needs the San Salvacion plan and a date after 1 January 2002. San Salvacion's treaty partners will be called to its defence.", "ac_ucw_can_start_war = yes OR = { date > 2003.5.31 AND = { has_country_flag = ac_ucw_war_plan_ready date > 2001.12.31 } }", "ac_ucw_start_war = yes", cost=25, visible=eru, ai=0)
    decision("ac_ucw_fallout", "ac_ucw_eru_continental_accord", "Sign a continental accord", "Requires grievance below 25, no mobilized reserves and a date after 1 January 2002. Erusea renounces force over the fallout. The Continental War is averted. Provisional gameplay: in the official chronology the war happens.", peace + " check_variable = { ac_ucw_grievance < 25 } NOT = { has_country_flag = ac_ucw_eru_mobilized } date > 2001.12.31", "ac_ucw_avert_war = yes", cost=100, visible=eru, ai=0)
    decision("ac_ucw_fallout", "ac_ucw_fcu_relief_corridors", "Open relief corridors", "Coordinate relief convoys: refugee pressure -10, recovery +5. Once every 180 days.", peace + " check_variable = { ac_ucw_pressure > 9 }", changes(0, -10, 5), visible=fcu, cooldown=180, single=False, ai=1)
    decision("ac_ucw_fallout", "ac_ucw_fcu_mediate", "Offer Erusea mediation", "Propose talks on refugees and reconstruction credit. Erusea may accept or refuse. Once every 365 days. Provisional gameplay.", peace + " country_exists = ERU", "ERU = { country_event = { id = ac_ucw.13 days = 1 } }", cost=50, visible=fcu, cooldown=365, single=False, ai=1)
    decision("ac_ucw_fallout", "ac_ucw_fcu_garrison_stonehenge", "Garrison Stonehenge", "Requires a completed Stonehenge. San Salvacion receives a defensive garrison; Erusea's grievance rises by 5. Provisional gameplay.", peace + " has_global_flag = ac_ucw_stonehenge_operational country_exists = SNS", "SNS = { add_ideas = ac_ucw_stonehenge_garrison }\n" + scoped("ERU", changes(5)), cost=75, visible=fcu, ai=1)
    decision("ac_ucw_fallout", "ac_ucw_fcu_draft_charter", "Draft an allied charter", "Requires Erusea's reserves to be mobilized. If Erusea attacks, the allied command forms at once instead of waiting for the recorded date of 22 August 2003. Provisional gameplay.", peace + " country_exists = ERU ERU = { has_country_flag = ac_ucw_eru_mobilized }", "set_country_flag = ac_ucw_isaf_prepared", visible=fcu, ai=1)
    effect("ac_ucw_avert_war", gonce("ac_ucw_war_averted", "news_event = { id = ac_ucw.25 days = 1 }", "ac_ucw_can_start_war = yes"))
    brief(25, "A continental accord", "Erusea and its neighbours have signed an accord renouncing force over the Ulysses fallout. In the official chronology the Usean Continental War begins in 2003. In this campaign it has been averted: a provisional gameplay branch.", picture="GFX_report_event_treaty_2")


def build_war():
    effect("ac_ucw_start_war", block("if", """limit = { ac_ucw_can_start_war = yes }
set_global_flag = ac_ucw_war_started
declare_war_on = { target = SNS type = annex_everything }
add_ideas = ac_ucw_eru_war_footing
FCU = { set_variable = { ac_ucw_stage_weeks = 0 } }
news_event = { id = ac_ucw.20 days = 1 }"""))
    brief(20, "Erusea invades San Salvacion", "The official chronology records that Erusea invaded neutral San Salvacion in the summer of 2003 and seized Stonehenge. In this campaign San Salvacion belongs to Central Usea's treaty organization from 1991, so its partners are called to its defence. The exact start date is provisional gameplay.")
    effect("ac_ucw_seize_stonehenge", gonce("ac_ucw_stonehenge_seized", """news_event = { id = ac_ucw.40 days = 1 }
if = {
    limit = { has_global_flag = ac_ucw_stonehenge_operational }
""" + "\n".join("    " + line for line in (scoped("ERU", "add_ideas = ac_ucw_stonehenge_railguns") + scoped("FCU", "add_ideas = ac_ucw_under_stonehenge")).splitlines()) + "\n}"))
    # Ground recapture completes the Stonehenge stage as well, so later checks see one state.
    effect("ac_ucw_destroy_stonehenge", gonce("ac_ucw_stonehenge_destroyed", "set_global_flag = ac_ucw_stage_stonehenge\nnews_event = { id = ac_ucw.44 days = 1 }\n" + scoped("ERU", "remove_ideas = ac_ucw_stonehenge_railguns") + scoped("FCU", "remove_ideas = ac_ucw_under_stonehenge\nset_variable = { ac_ucw_stage_weeks = 0 }"), "has_global_flag = ac_ucw_stonehenge_seized"))
    brief(40, "Stonehenge turns on the sky", "The official chronology records that Erusea seized Stonehenge and turned its railguns, built to destroy Ulysses fragments, against aircraft. Allied air operations over the continent now face the battery's fire.")
    effect("ac_ucw_eru_war_tick", """# Provisional window: the Chronicle records only the summer of 2003.
if = {
    limit = { is_ai = yes ac_ucw_can_start_war = yes date > 2003.6.20 NOT = { has_global_flag = ac_ucw_late_calendar } check_variable = { ac_ucw_grievance > 24 } }
    ac_ucw_start_war = yes
}
if = {
    limit = { ac_ucw_war_running = yes }
    if = { limit = { NOT = { has_global_flag = ac_ucw_stonehenge_seized } ac_ucw_stonehenge_held_by_erusea = yes } ac_ucw_seize_stonehenge = yes }
    # A playtest seizure leaves the map unchanged; only a real Erusean hold can later be lost.
    if = { limit = { has_global_flag = ac_ucw_stonehenge_simulated ac_ucw_stonehenge_held_by_erusea = yes } clr_global_flag = ac_ucw_stonehenge_simulated }
    if = { limit = { has_global_flag = ac_ucw_stonehenge_seized NOT = { has_global_flag = ac_ucw_stonehenge_simulated } ac_ucw_stonehenge_held_by_erusea = no } ac_ucw_destroy_stonehenge = yes }
    if = {
        limit = { is_ai = yes has_global_flag = ac_ucw_stage_stonehenge NOT = { has_country_flag = ac_ucw_armistice_sought } country_exists = FCU FCU = { check_variable = { ac_ucw_stage_weeks > 40 } } }
        set_country_flag = ac_ucw_armistice_sought
        FCU = { country_event = { id = ac_ucw.45 days = 1 } }
    }
}""")
    effect("ac_ucw_form_isaf", gonce("ac_ucw_isaf_formed", """if = { limit = { is_faction_leader = yes } set_faction_name = ac_ucw_isaf_faction }
if = { limit = { country_exists = ERU NOT = { has_war_with = ERU } } declare_war_on = { target = ERU type = topple_government } }
add_ideas = ac_ucw_isaf_command
set_variable = { ac_ucw_stage_weeks = 0 }
news_event = { id = ac_ucw.31 days = 1 }
""" + scoped("NPT", block("if", "limit = { NOT = { is_in_faction_with = FCU } NOT = { has_war_with = FCU } has_capitulated = no }\ncountry_event = { id = ac_ucw.32 days = 2 }")),
        "original_tag = FCU ac_ucw_war_running = yes has_capitulated = no"))
    loc("ac_ucw_isaf_faction", "Independent State Allied Forces")
    event(30, "The Independent State Allied Forces", "The official chronology records that Central Usea demanded Erusea's withdrawal from Stonehenge and San Salvacion, and that FCU President Robert Sinclair established the Independent State Allied Forces on 22 August 2003. Our treaty organization becomes ISAF's command.", [
        ("Found ISAF.", "ac_ucw_form_isaf = yes", "", 100)], trigger_text="ac_ucw_war_running = yes", picture="GFX_report_event_ose_war_committee")
    brief(31, "ISAF is founded", "Central Usea has founded the Independent State Allied Forces to drive Erusea out of San Salvacion. The official chronology dates its founding to 22 August 2003.", picture="GFX_report_event_treaty_1")
    event(32, "ISAF asks for North Point", "ISAF has invited North Point to join the allied command. In the official chronology ISAF's headquarters moves to North Point on 16 September 2004. Joining commits the island to the war; declining keeps its neutrality, which is a provisional alternative.", [
        ("Join ISAF.", "if = { limit = { has_global_flag = ac_ucw_stage_north_point ac_ucw_war_running = yes } add_ideas = ac_ucw_npt_isaf_rear_base }\n" + scoped("FCU", "add_to_faction = NPT\ncountry_event = { id = ac_ucw.33 days = 1 }"), "", 80),
        ("Keep our neutrality.", scoped("FCU", "country_event = { id = ac_ucw.34 days = 1 }"), "", 20)], picture="GFX_report_event_treaty_2")
    event(33, "North Point joins ISAF", "North Point has joined the allied command. Its harbours and airfields are open to ISAF.", [("Welcome them.", "", "", 100)])
    event(34, "North Point declines", "North Point has declined to join ISAF for now. Its government is willing to talk again if the war turns.", [("Note the answer.", "", "", 100)], picture="GFX_report_event_bad_news_1")
    effect("ac_ucw_fcu_war_tick", """if = {
    limit = { ac_ucw_war_running = yes NOT = { has_global_flag = ac_ucw_isaf_formed } NOT = { has_country_flag = ac_ucw_isaf_offered } OR = { date > 2003.8.21 has_country_flag = ac_ucw_isaf_prepared } }
    set_country_flag = ac_ucw_isaf_offered
    country_event = { id = ac_ucw.30 days = 1 }
}
if = {
    limit = { ac_ucw_war_running = yes has_global_flag = ac_ucw_isaf_formed }
    add_to_variable = { ac_ucw_stage_weeks = 1 }
    clamp_variable = { var = ac_ucw_stage_weeks min = 0 max = 520 }
}
if = {
    limit = { is_ai = yes ac_ucw_war_running = yes }
""" + "\n".join("    if = { limit = { ac_ucw_stage_%s_ready = yes check_variable = { ac_ucw_stage_weeks > %d } } ac_ucw_stage_%s = yes }" % (s, ai - 1, s) for s, _, _, ai, *_ in STAGES) + "\n}")
    previous = "has_global_flag = ac_ucw_isaf_formed"
    for name, title, desc, ai, human, news, extra, picture in STAGES:
        ready = previous + "\nNOT = { has_global_flag = ac_ucw_stage_%s }\n%s" % (name, extra)
        trigger("ac_ucw_stage_%s_ready" % name, "original_tag = FCU\nac_ucw_war_running = yes\n" + ready.strip())
        # The Stonehenge stage reuses the destruction effect, which reports itself.
        report = "\nnews_event = { id = ac_ucw.%d days = 1 }" % news if news else ""
        effect("ac_ucw_stage_%s" % name, gonce("ac_ucw_stage_" + name, STAGE_EFFECTS[name] + "\nset_variable = { ac_ucw_stage_weeks = 0 }" + report, "ac_ucw_stage_%s_ready = yes" % name))
        decision("ac_ucw_war", "ac_ucw_order_" + name, title, desc, "ac_ucw_stage_%s_ready = yes check_variable = { ac_ucw_stage_weeks > %d }" % (name, human - 1), "ac_ucw_stage_%s = yes" % name, cost=25, visible="original_tag = FCU has_global_flag = ac_ucw_isaf_formed", ai=0)
        previous = "has_global_flag = ac_ucw_stage_" + name
    brief(41, "ISAF falls back to Los Canas", "The official chronology records that Stonehenge pushed ISAF back to Los Canas and that its first offensive against the battery failed on 14 September 2003. ISAF is regrouping for a long war.")
    brief(42, "ISAF headquarters moves to North Point", "The official chronology records that ISAF established its headquarters in North Point on 16 September 2004. From the island, the allied command prepares its return to the continent.", picture="GFX_report_event_ose_war_committee")
    brief(43, "ISAF lands on the Usean continent", "The official chronology records that ISAF landed on the Usean continent on 24 January 2005. The counteroffensive has begun.")
    brief(44, "Stonehenge is destroyed", "The official chronology records that ISAF destroyed Stonehenge on 2 April 2005; seven of its eight batteries were knocked out. Allied air power is free of the railguns.")
    for number, (flag, when, title, desc, needs) in enumerate(BRIEFS, 70):
        brief(number, title, desc)
    # A late load marks past briefs <flag>_done so they are never replayed.
    effect("ac_ucw_chronicle_tick", "\n".join(
        gonce(flag, "news_event = { id = ac_ucw.%d days = 1 }" % number,
              "ac_ucw_war_running = yes date > %s %s NOT = { has_global_flag = %s_done }" % (when, needs, flag)).rstrip()
        for number, (flag, when, title, desc, needs) in enumerate(BRIEFS, 70)))
    armistice = "\n".join("if = { limit = { country_exists = %s has_war_with = %s } white_peace = %s }" % (tag, tag, tag) for tag in ENEMIES)
    effect("ac_ucw_armistice", block("if", "limit = { original_tag = ERU ac_ucw_war_running = yes }\n" + armistice + "\nac_ucw_record_stalemate = yes"))
    decision("ac_ucw_war", "ac_ucw_eru_seek_armistice", "Seek an armistice", "Requires ISAF's landing on the continent. Ask ISAF for an armistice along the current lines. If accepted, the war ends in a negotiated stalemate. Provisional gameplay.", "ac_ucw_war_running = yes has_global_flag = ac_ucw_stage_counteroffensive country_exists = FCU", "FCU = { country_event = { id = ac_ucw.45 days = 1 } }", cost=50, visible="original_tag = ERU", cooldown=180, single=False, ai=0)
    decision("ac_ucw_war", "ac_ucw_fcu_offer_armistice", "Offer Erusea an armistice", "Requires the fall back to Los Canas. Offer an armistice along the current lines. If Erusea accepts, the war ends in a negotiated stalemate. Provisional gameplay.", "ac_ucw_war_running = yes has_global_flag = ac_ucw_stage_los_canas country_exists = ERU", "ERU = { country_event = { id = ac_ucw.46 days = 1 } }", cost=50, visible="original_tag = FCU has_global_flag = ac_ucw_isaf_formed", cooldown=180, single=False, ai=0)
    event(45, "Erusea asks for an armistice", "Erusea proposes an armistice along the current front lines. Accepting ends the war without a decision; refusing continues the campaign. Provisional gameplay.", [
        ("Accept the armistice.", scoped("ERU", "ac_ucw_armistice = yes"), "ac_ucw_war_running = yes", 20),
        ("Refuse and fight on.", scoped("ERU", "country_event = { id = ac_ucw.47 days = 1 }"), "", 80)], trigger_text="ac_ucw_war_running = yes", picture="GFX_report_event_treaty_1")
    event(46, "ISAF offers an armistice", "ISAF proposes an armistice along the current front lines. Accepting ends the war without a decision; refusing continues the campaign. Provisional gameplay.", [
        ("Accept the armistice.", "ac_ucw_armistice = yes", "ac_ucw_war_running = yes", 15),
        ("Refuse and fight on.", scoped("FCU", "country_event = { id = ac_ucw.47 days = 1 }"), "", 85)], trigger_text="ac_ucw_war_running = yes", picture="GFX_report_event_treaty_1")
    event(47, "The armistice is refused", "The other side has refused an armistice. The war continues.", [("Then we fight on.", "", "", 100)], picture="GFX_report_event_bad_news_1")


def build_outcomes():
    # Stage spirits only make sense while the war runs; every ending clears them.
    effect("ac_ucw_end_war_spirits", scoped("FCU", "\n".join("remove_ideas = " + i for i in ("ac_ucw_isaf_command", "ac_ucw_isaf_fallback", "ac_ucw_isaf_north_point_hq", "ac_ucw_isaf_counteroffensive", "ac_ucw_under_stonehenge")))
           + scoped("ERU", "\n".join("remove_ideas = " + i for i in ("ac_ucw_eru_war_footing", "ac_ucw_eru_overstretched", "ac_ucw_stonehenge_railguns")))
           + scoped("NPT", "remove_ideas = ac_ucw_npt_isaf_rear_base"))
    effect("ac_ucw_record_isaf_victory", gonce("ac_ucw_outcome_isaf_victory", "ac_ucw_end_war_spirits = yes\nnews_event = { id = ac_ucw.50 days = 1 }\n" + scoped("FCU", "country_event = { id = ac_ucw.60 days = 7 }"), "ac_ucw_war_running = yes"))
    effect("ac_ucw_record_erusean_victory", gonce("ac_ucw_outcome_erusean_victory", "ac_ucw_end_war_spirits = yes\nnews_event = { id = ac_ucw.51 days = 1 }", "ac_ucw_war_running = yes"))
    effect("ac_ucw_record_stalemate", gonce("ac_ucw_outcome_stalemate", "ac_ucw_end_war_spirits = yes\nnews_event = { id = ac_ucw.52 days = 1 }", "ac_ucw_war_running = yes"))
    effect("ac_ucw_outcome_tick", block("if", """limit = { ac_ucw_war_running = yes }
if = { limit = { OR = { NOT = { country_exists = ERU } ERU = { has_capitulated = yes } } } ac_ucw_record_isaf_victory = yes }
else_if = { limit = { OR = { NOT = { country_exists = FCU } FCU = { has_capitulated = yes } } } ac_ucw_record_erusean_victory = yes }
else_if = { limit = { has_global_flag = ac_ucw_isaf_formed ERU = { NOT = { has_war_with = FCU } } } ac_ucw_record_stalemate = yes }"""))
    brief(50, "Farbanti falls", "The official chronology records that Farbanti fell and Erusea surrendered on 19 September 2005, ending the Usean Continental War. In this campaign ISAF has won the war.", picture="GFX_report_event_flag_osea_1")
    brief(51, "Erusea wins the Continental War", "Central Usea's command has collapsed and Erusea dominates the continent. In the official chronology ISAF wins the war; this outcome is a provisional gameplay branch.", picture="GFX_report_event_bad_news_2")
    brief(52, "An armistice in Usea", "The Usean Continental War has ended in an armistice along the front lines, with no decision on the battlefield. In the official chronology ISAF wins the war; this outcome is a provisional gameplay branch.", picture="GFX_report_event_treaty_2")
    event(60, "Megalith", "The official chronology records that young Erusean officers seized Megalith on 26 September 2005, a fortress built to bring down orbiting Ulysses fragments. ISAF must take the fortress before it can be used.", [
        ("Send ISAF into Megalith.", "set_global_flag = ac_ucw_megalith_active\nadd_timed_idea = { idea = ac_ucw_megalith_threat days = 14 }\ncountry_event = { id = ac_ucw.61 days = 14 }", "", 100)], picture="GFX_report_event_excalibur_1")
    effect("ac_ucw_destroy_megalith", gonce("ac_ucw_megalith_destroyed", "clr_global_flag = ac_ucw_megalith_active\nnews_event = { id = ac_ucw.62 days = 1 }\n" + scoped("ERU", "add_ideas = ac_ucw_eru_provisional_government"), "has_global_flag = ac_ucw_megalith_active"))
    event(61, "Megalith is destroyed", "ISAF has destroyed Megalith. Erusea's surrender stands.", [("Close the operation.", "ac_ucw_destroy_megalith = yes", "", 100)], picture="GFX_report_event_excalibur_1")
    brief(62, "Erusea's provisional government", "The official chronology records that after Megalith was destroyed, Erusea formed a provisional autonomous government under ISAF oversight. The government in office stays in place; the arrangement is shown as a national spirit, not a change of borders or ideology.", picture="GFX_report_event_treaty_1")
    effect("ac_ucw_assessment_tick", block("if", """limit = {
    has_country_flag = ac_ucw_started
    NOT = { has_country_flag = ac_ucw_assessment_sent }
    OR = {
        has_global_flag = ac_ucw_megalith_destroyed
        has_global_flag = ac_ucw_outcome_erusean_victory
        has_global_flag = ac_ucw_outcome_stalemate
        AND = { has_global_flag = ac_ucw_war_averted date > 2004.12.31 }
        date > 2005.12.30
    }
}
set_country_flag = ac_ucw_assessment_sent
set_global_flag = ac_ucw_2005_assessed
country_event = { id = ac_ucw.90 days = 1 }"""))
    event(90, "Usea at the end of the war", "The record for 2005: refugee pressure [?ac_ucw_pressure|.0], fallout recovery [?ac_ucw_recovery|.0]. [GetUcwOutcome] This is the end of the authored Usean chronology; the campaign continues.", [("Carry the record forward.", "", "", 100)], picture="GFX_report_event_treaty_2")


STAGES = [
    ("los_canas", "Fall back to Los Canas", "Requires ISAF. Pull the allied armies back to Los Canas and regroup (official chronology, 14 September 2003). Grants defensive bonuses. Available one week after ISAF forms; the AI takes it after three weeks.", 3, 1, 41, "", "GFX_report_event_blk_army_attack"),
    ("north_point", "Move ISAF headquarters to North Point", "Requires the fall back to Los Canas. Move the allied command to North Point (official chronology, 16 September 2004). Available after 26 weeks; the AI takes it after 52.", 52, 26, 42, "", "GFX_report_event_ose_war_committee"),
    ("counteroffensive", "Land on the Usean continent", "Requires the North Point headquarters. Begin the counteroffensive (official chronology, 24 January 2005). Available after 9 weeks; the AI takes it after 18.", 18, 9, 43, "", "GFX_report_event_blk_army_attack"),
    ("stonehenge", "Strike Stonehenge", "Requires the landing and an Erusean-held Stonehenge. Destroy the railguns from the air (official chronology, 2 April 2005). Available after 4 weeks; the AI takes it after 10. Retaking San Salvacion's capital state destroys the battery as well.", 10, 4, 0, "has_global_flag = ac_ucw_stonehenge_seized\nNOT = { has_global_flag = ac_ucw_stonehenge_destroyed }", "GFX_report_event_excalibur_1"),
]
STAGE_EFFECTS = {
    "los_canas": "add_ideas = ac_ucw_isaf_fallback\n" + scoped("ERU", "add_timed_idea = { idea = ac_ucw_eru_offensive days = 180 }"),
    "north_point": "remove_ideas = ac_ucw_isaf_fallback\nadd_ideas = ac_ucw_isaf_north_point_hq\n" + scoped("NPT", block("if", "limit = { OR = { has_country_flag = ac_npt_hosts_isaf is_in_faction_with = FCU } }\nadd_ideas = ac_ucw_npt_isaf_rear_base") + block("else_if", "limit = { NOT = { has_war_with = FCU } has_capitulated = no }\ncountry_event = { id = ac_ucw.32 days = 2 }")),
    "counteroffensive": "remove_ideas = ac_ucw_isaf_north_point_hq\nadd_ideas = ac_ucw_isaf_counteroffensive\n" + scoped("ERU", "add_ideas = ac_ucw_eru_overstretched"),
    "stonehenge": "ac_ucw_destroy_stonehenge = yes",
}
BRIEFS = [
    ("ac_ucw_brief_shezna", "2004.10.9", "The Mount Shezna radar", "The official chronology records that the Mount Shezna radar was destroyed on 10 October 2004 to cover ISAF's retreat from Saint Ark.", "has_global_flag = ac_ucw_stage_north_point"),
    ("ac_ucw_brief_comberth", "2004.11.22", "The Aegir fleet at Comberth Harbor", "The official chronology records that ISAF sank Erusea's Aegir fleet at Comberth Harbor on 23 November 2004.", "has_global_flag = ac_ucw_stage_north_point"),
    ("ac_ucw_brief_comona", "2004.12.30", "Air battle over the Comona Islands", "The official chronology records a large air battle over the Comona Islands on 31 December 2004.", "has_global_flag = ac_ucw_stage_north_point"),
    ("ac_ucw_brief_istas", "2005.2.27", "Istas Fortress and the Tango Line", "The official chronology records that ISAF took Istas Fortress and breached the Tango Line on 28 February 2005.", "has_global_flag = ac_ucw_stage_counteroffensive"),
    ("ac_ucw_brief_engineers", "2005.3.13", "The Stonehenge engineers escape", "The official chronology records that the Stonehenge engineers and their families escaped Erusean custody on 14 March 2005.", "has_global_flag = ac_ucw_stage_counteroffensive"),
    ("ac_ucw_brief_ice_creek", "2005.6.17", "The northern landing at Ice Creek", "The official chronology records ISAF's northern landing at Ice Creek on 18 June 2005.", "has_global_flag = ac_ucw_stage_counteroffensive"),
    ("ac_ucw_brief_san_salvacion", "2005.7.9", "San Salvacion is liberated", "The official chronology records the liberation of San Salvacion on 10 July 2005.", "has_global_flag = ac_ucw_stage_counteroffensive ac_ucw_stonehenge_held_by_erusea = no"),
    ("ac_ucw_brief_whiskey", "2005.8.14", "The Whiskey Corridor", "The official chronology records that ISAF breached the Whiskey Corridor on 15 August 2005.", "has_global_flag = ac_ucw_stage_counteroffensive"),
]


def build_ideas():
    rows = [
        ("ac_ucw_refugee_relief", "Refugee Relief Camps", "Relief camps strain construction and public patience. Provisional gameplay cost.", "generic_increased_immigration", "stability_factor = -0.02\nproduction_speed_buildings_factor = -0.03"),
        ("ac_ucw_border_controls", "Border Controls", "The closed border relieves the ministries and hardens public opinion. Provisional gameplay.", "generic_decreased_immigration", "stability_factor = 0.02\nwar_support_factor = 0.03"),
        ("ac_ucw_eru_rearmament", "Erusean Rearmament", "Factories and training grounds are rebuilt for a war Erusea says it does not want. Provisional gameplay.", "generic_aggressive_military_thought", "industrial_capacity_factory = 0.05\ntraining_time_factor = -0.05"),
        ("ac_ucw_eru_aegir_fleet", "The Aegir Fleet", "Erusea's surface fleet is rebuilt as the Aegir fleet. Provisional gameplay.", "generic_expeditionary_army", "naval_damage_factor = 0.05\nnavy_org_factor = 0.05"),
        ("ac_ucw_eru_mobilization", "Reserves Mobilized", "Reservists stand ready along the San Salvacion frontier. Provisional gameplay.", "generic_tank_advance", "conscription_factor = 0.1\nconsumer_goods_factor = 0.05"),
        ("ac_ucw_eru_war_footing", "Continental War Footing", "Erusea's armies march on San Salvacion. Provisional gameplay.", "generic_tank_advance", "army_attack_factor = 0.05\nwar_support_factor = 0.05"),
        ("ac_ucw_eru_offensive", "The Continental Offensive", "Erusean armies press the retreating allies. Expires after 180 days. Provisional gameplay.", "generic_aggressive_military_thought", "army_attack_factor = 0.05\nplanning_speed = 0.1"),
        ("ac_ucw_eru_overstretched", "An Overstretched Front", "ISAF's landing forces Erusea to defend a continent-wide front. Provisional gameplay.", "generic_logistical_destruction", "army_defence_factor = -0.05\nsupply_consumption_factor = 0.05"),
        ("ac_ucw_stonehenge_railguns", "Stonehenge Railguns", "The railguns built against Ulysses fragments now fire on enemy aircraft. Provisional gameplay values.", "excalibur_fire_idea", "enemy_army_bonus_air_superiority_factor = -0.25\nair_defence_factor = 0.1"),
        ("ac_ucw_under_stonehenge", "Under Stonehenge's Guns", "Allied air operations over the continent fly within the battery's reach. Provisional gameplay values.", "generic_airstrike", "air_mission_efficiency = -0.15\nair_accidents_factor = 0.1"),
        ("ac_ucw_stonehenge_garrison", "Stonehenge Garrison", "Allied troops guard the Stonehenge site. Provisional gameplay.", "generic_defensive_army", "army_core_defence_factor = 0.1"),
        ("ac_ucw_isaf_command", "ISAF Command", "The Independent State Allied Forces coordinate the allied war effort.", "OSE_joint_allied_command", "army_org_factor = 0.05\nplanning_speed = 0.1"),
        ("ac_ucw_isaf_fallback", "Holding at Los Canas", "ISAF trades ground for time while it regroups. Provisional gameplay values.", "generic_defensive_army", "army_defence_factor = 0.1\narmy_attack_factor = -0.05"),
        ("ac_ucw_isaf_north_point_hq", "Headquarters at North Point", "From North Point, ISAF rebuilds its air wings and plans the return. Provisional gameplay values.", "UTO_president", "air_attack_factor = 0.05\nindustrial_capacity_factory = 0.05"),
        ("ac_ucw_isaf_counteroffensive", "The Counteroffensive", "ISAF is back on the continent and on the attack. Provisional gameplay values.", "generic_expeditionary_army", "army_attack_factor = 0.1\nnaval_speed_factor = 0.05"),
        ("ac_ucw_npt_isaf_rear_base", "ISAF Rear Base", "North Point's harbours and airfields serve the allied command. Provisional gameplay values.", "UTO_member", "industrial_capacity_factory = 0.05\nair_defence_factor = 0.05"),
        ("ac_ucw_megalith_threat", "The Megalith Threat", "While Megalith is held, its threat hangs over the allied capitals. Expires after 14 days.", "excalibur_fire_idea", "stability_factor = -0.05"),
        ("ac_ucw_eru_provisional_government", "Provisional Autonomous Government", "Erusea governs itself under ISAF oversight (official chronology, 26 September 2005). The government in office remains; the modifiers are provisional gameplay.", "cold_war_eco", "stability_factor = 0.05\nwar_support_factor = -0.15\npolitical_power_factor = -0.1"),
        ("ac_ucw_eru_victors_order", "The Victor's Order", "Erusea dictates the continental order. Provisional gameplay branch.", "generic_aggressive_military_thought", "political_power_factor = 0.1\nstability_factor = -0.05"),
        ("ac_ucw_armistice_line", "The Armistice Line", "An armistice holds along the front lines. Provisional gameplay branch.", "generic_defensive_army", "army_core_defence_factor = 0.1\nconsumer_goods_factor = 0.03"),
        ("ac_ucw_continental_peace", "A Continental Peace", "Usea has kept the peace after Ulysses. Provisional gameplay branch.", "CNEA_member", "stability_factor = 0.05\nproduction_speed_buildings_factor = 0.05"),
    ]
    for row in rows:
        idea(*row)
    OUTPUT["common/ideas/ac_ucw.txt"] = block("ideas", block("country", "\n".join(IDEAS)))
    OUTPUT["common/opinion_modifiers/ac_ucw.txt"] = block("opinion_modifiers", block("ac_ucw_mediation", "value = 15"))
    loc("ac_ucw_mediation", "Fallout mediation")


I = {
    "globe": "GFX_focus_generic_globe_usea", "diplo": "GFX_focus_generic_diplomacy_osea", "defend": "GFX_focus_generic_army_defensive",
    "security": "GFX_focus_generic_army_internal_security", "expedition": "GFX_focus_generic_army_expeditionary",
    "fighter": "GFX_focus_generic_fighter_weapons_school", "bomber": "GFX_focus_generic_bomber_training_school",
    "cas": "GFX_focus_generic_cas_training_school", "industry": "GFX_focus_generic_infantry_equipment_research",
    "steel": "GFX_focus_generic_extract_steel", "arms": "GFX_focus_generic_purchase_osean_arms", "guard": "GFX_focus_generic_army_palace_guard",
}


def outcome_available(*outcomes):
    return "OR = { " + " ".join("has_global_flag = ac_ucw_outcome_" + o for o in outcomes) + " }"


def build_trees():
    war = "has_global_flag = ac_ucw_war_started"
    f = focus
    f("ERU", "after_ulysses", "After Ulysses", "Count the damage of the fallout and set the government's priorities for the new decade.", 10, 0, I["globe"], reward=changes(0, 0, 5) + "\nadd_political_power = 50")
    f("ERU", "close_the_border", "Close the Border", "Keep refugee columns out of Erusea. Refugee pressure -10, grievance +5.", 6, 1, I["security"], ["after_ulysses"], reward=changes(5, -10) + "\nadd_ideas = ac_ucw_border_controls", excludes=["refugee_quotas"], ai=40)
    f("ERU", "refugee_quotas", "Managed Refugee Quotas", "Admit refugees under quotas. Refugee pressure +5, recovery -3, grievance -10. Provisional gameplay.", 10, 1, I["diplo"], ["after_ulysses"], reward=changes(-10, 5, -3), excludes=["close_the_border"], ai=5)
    f("ERU", "rebuild_farbanti", "Rebuild Farbanti", "Repair the capital's services first. Recovery +10.", 14, 1, I["steel"], ["after_ulysses"], reward=changes(0, 0, 10) + "\nadd_stability = 0.03")
    f("ERU", "national_grievance", "The Nation's Grievance", "Tell Erusea that its suffering was ignored. Grievance +10, war support +3 percentage points.", 7, 2, I["guard"], ["close_the_border", "refugee_quotas"], reward=changes(10) + "\nadd_war_support = 0.03", excludes=["continental_dialogue"], ai=40)
    f("ERU", "continental_dialogue", "Continental Dialogue", "Seek a regional settlement of the fallout. Grievance -15. Provisional gameplay.", 13, 2, I["diplo"], ["close_the_border", "refugee_quotas"], reward=changes(-15) + "\nadd_political_power = -25", excludes=["national_grievance"], ai=5)
    f("ERU", "army_modernization", "Modernize the Erusean Army", "Rebuild the army's training and industry.", 7, 3, I["industry"], ["national_grievance"], reward="army_experience = 15\nadd_ideas = ac_ucw_eru_rearmament")
    f("ERU", "aegir_fleet", "The Aegir Fleet", "Rebuild the surface fleet. The official chronology records the Aegir fleet's loss at Comberth Harbor in November 2004.", 5, 4, I["expedition"], ["army_modernization"], reward="navy_experience = 20\nadd_ideas = ac_ucw_eru_aegir_fleet")
    f("ERU", "air_arm", "The Erusean Air Arm", "Train fighter and strike squadrons.", 9, 4, I["fighter"], ["army_modernization"], reward="air_experience = 20")
    f("ERU", "mobilize", "Mobilize the Reserves", "Call up the reserves along the San Salvacion frontier. Grievance +5.", 7, 5, I["defend"], ["aegir_fleet", "air_arm"], reward=changes(5) + "\nset_country_flag = ac_ucw_eru_mobilized\nadd_ideas = ac_ucw_eru_mobilization")
    f("ERU", "san_salvacion_plan", "Plan for San Salvacion", "Prepare the invasion plan. Unlocks an invasion before the summer of 2003 if grievance is at least 70. Provisional gameplay.", 7, 6, I["guard"], ["mobilize"], reward="set_country_flag = ac_ucw_war_plan_ready\narmy_experience = 10")
    f("ERU", "seize_stonehenge", "Seize Stonehenge", "Requires the war. Take the railgun battery intact.", 7, 7, I["expedition"], ["san_salvacion_plan"], war, "army_experience = 15\nadd_war_support = 0.03", cost=3)
    f("ERU", "hold_the_continent", "Hold the Continent", "Requires ISAF's fall back to Los Canas. Dig in against the allied return.", 7, 8, I["defend"], ["seize_stonehenge"], "has_global_flag = ac_ucw_stage_los_canas", "add_stability = 0.03\narmy_experience = 10", cost=3)
    f("ERU", "megalith", "Megalith", "Requires the war. Fund the fortress built to bring down orbiting Ulysses fragments. No construction date is published, so this timing is provisional gameplay.", 7, 9, I["bomber"], ["hold_the_continent"], war, "add_political_power = 50\nair_experience = 10", cost=3)
    f("ERU", "refugee_accord", "Refugee Accord", "Agree a regional refugee accord with Central Usea. Grievance -10, refugee pressure -10. Provisional gameplay.", 13, 3, I["diplo"], ["continental_dialogue"], "NOT = { %s }" % war, changes(-10, -10) + "\n" + scoped("FCU", "add_opinion_modifier = { target = ERU modifier = ac_ucw_mediation }"))
    f("ERU", "reconstruction_bonds", "Reconstruction Bonds", "Finance recovery at home. Recovery +10.", 13, 4, I["steel"], ["refugee_accord"], reward=changes(0, 0, 10) + "\nif = { limit = { ac_econ_ready = yes } ac_econ_set_reconstruction = yes }")
    f("ERU", "arms_talks", "Usean Arms Talks", "Join talks on continental arms limits. Grievance -10. Provisional gameplay.", 13, 5, I["diplo"], ["reconstruction_bonds"], "NOT = { %s }" % war, changes(-10) + "\nadd_war_support = -0.03")
    f("ERU", "continental_accord", "A Continental Accord", "Requires grievance below 25 and a date after 1 January 2002. Renounce force over the fallout. The Continental War is averted. Provisional gameplay.", 13, 6, I["globe"], ["arms_talks"], "NOT = { %s } NOT = { has_global_flag = ac_ucw_war_averted } check_variable = { ac_ucw_grievance < 25 } date > 2001.12.31 NOT = { has_country_flag = ac_ucw_eru_mobilized }" % war, "if = { limit = { ac_ucw_can_start_war = yes } ac_ucw_avert_war = yes add_ideas = ac_ucw_continental_peace }")
    f("ERU", "provisional_government", "The Provisional Government", "Requires ISAF victory. Govern under ISAF oversight (official chronology, 26 September 2005).", 5, 11, I["diplo"], available=outcome_available("isaf_victory"), reward="add_political_power = 50\nadd_stability = 0.05", cost=3)
    f("ERU", "rebuild_under_oversight", "Rebuild Under Oversight", "Rebuild the country with allied credit. Provisional gameplay.", 5, 12, I["steel"], ["provisional_government"], reward=changes(0, -10, 10), cost=3)
    f("ERU", "victors_order", "The Victor's Order", "Requires Erusean victory. Dictate the continental order. Provisional gameplay.", 9, 11, I["guard"], available=outcome_available("erusean_victory"), reward="add_ideas = ac_ucw_eru_victors_order", cost=3)
    f("ERU", "garrison_the_continent", "Garrison the Continent", "Hold what the war has won. Provisional gameplay.", 9, 12, I["defend"], ["victors_order"], reward="army_experience = 15", cost=3)
    f("ERU", "armistice_line", "The Armistice Line", "Requires a stalemate or an averted war. Fortify the peace. Provisional gameplay.", 13, 11, I["defend"], available="OR = { has_global_flag = ac_ucw_outcome_stalemate has_global_flag = ac_ucw_war_averted }", reward="add_ideas = ac_ucw_armistice_line", cost=3)
    f("ERU", "recovery_decade", "A Decade of Recovery", "Turn the country to reconstruction. Provisional gameplay.", 13, 12, I["steel"], ["armistice_line"], reward=changes(-10, -10, 15), cost=3)

    f("FCU", "after_ulysses", "After Ulysses", "Count the cost of the fallout across the treaty organization.", 10, 0, I["globe"], reward=changes(0, 0, 5) + "\nadd_political_power = 50")
    f("FCU", "relief_camps", "Refugee Relief", "Receive displaced families. Refugee pressure +5, recovery +5, stability -2 percentage points.", 6, 1, I["diplo"], ["after_ulysses"], reward=changes(0, 5, 5) + "\nadd_stability = -0.02")
    f("FCU", "stonehenge_custody", "Custody of Stonehenge", "Requires a completed Stonehenge. Place the battery under treaty guard. Provisional gameplay.", 10, 1, I["defend"], ["after_ulysses"], "has_global_flag = ac_ucw_stonehenge_operational country_exists = SNS", "SNS = { add_ideas = ac_ucw_stonehenge_garrison }")
    f("FCU", "continental_economy", "A Continental Economy", "Coordinate recovery credit across the treaty organization. Recovery +10.", 14, 1, I["steel"], ["after_ulysses"], reward=changes(0, 0, 10) + "\nif = { limit = { ac_econ_ready = yes } ac_econ_set_reconstruction = yes }")
    f("FCU", "mediation", "Mediate with Erusea", "Offer Erusea talks on the fallout. Provisional gameplay.", 6, 2, I["diplo"], ["relief_camps"], "NOT = { %s } country_exists = ERU" % war, "ERU = { country_event = { id = ac_ucw.13 days = 1 } }")
    f("FCU", "uto_readiness", "Treaty Readiness Review", "Review the treaty organization's forces.", 12, 2, I["industry"], ["stonehenge_custody", "continental_economy"], reward="army_experience = 10\nair_experience = 10")
    f("FCU", "early_warning", "Early-Warning Network", "Build radar and reconnaissance coverage of the Erusean frontier.", 12, 3, I["fighter"], ["uto_readiness"], reward="air_experience = 15")
    f("FCU", "draft_charter", "Draft an Allied Charter", "If Erusea attacks, the allied command forms at once. Provisional gameplay.", 12, 4, I["diplo"], ["early_warning"], reward="set_country_flag = ac_ucw_isaf_prepared")
    f("FCU", "peace_dividend", "The Peace Dividend", "Requires an averted war. Turn treaty spending to recovery. Provisional gameplay.", 16, 4, I["steel"], ["continental_economy"], "has_global_flag = ac_ucw_war_averted", changes(0, -10, 10) + "\nadd_ideas = ac_ucw_continental_peace")
    f("FCU", "found_isaf", "The Allied Command", "Requires ISAF. Put the allied armies under one command (official chronology, 22 August 2003).", 10, 5, I["guard"], ["mediation", "draft_charter"], "has_global_flag = ac_ucw_isaf_formed", "army_experience = 15\nadd_war_support = 0.05", cost=3)
    f("FCU", "hold_los_canas", "Hold Los Canas", "Requires the fall back to Los Canas. Fortify the last line.", 8, 6, I["defend"], ["found_isaf"], "has_global_flag = ac_ucw_stage_los_canas", "army_experience = 10\nadd_stability = 0.03", cost=3)
    f("FCU", "invite_north_point", "An Island Headquarters", "Ask North Point to host the allied command.", 12, 6, I["diplo"], ["found_isaf"], "country_exists = NPT", scoped("NPT", block("if", "limit = { NOT = { is_in_faction_with = FCU } NOT = { has_war_with = FCU } has_capitulated = no }\ncountry_event = { id = ac_ucw.32 days = 1 }")), cost=3)
    f("FCU", "north_point_hq", "Command from North Point", "Requires the North Point headquarters. Rebuild the allied air wings from the island.", 10, 7, I["fighter"], ["hold_los_canas", "invite_north_point"], "has_global_flag = ac_ucw_stage_north_point", "air_experience = 25", cost=3)
    f("FCU", "air_wings", "Rebuild the Air Wings", "Train new squadrons for the return.", 8, 8, I["bomber"], ["north_point_hq"], reward="air_experience = 20", cost=3)
    f("FCU", "amphibious_lift", "Amphibious Lift", "Assemble the shipping for a continental landing.", 12, 8, I["expedition"], ["north_point_hq"], reward="navy_experience = 20", cost=3)
    f("FCU", "landing", "Return to the Continent", "Requires the landing. Consolidate the beachheads.", 10, 9, I["expedition"], ["air_wings", "amphibious_lift"], "has_global_flag = ac_ucw_stage_counteroffensive", "army_experience = 20", cost=3)
    f("FCU", "strike_stonehenge", "Silence Stonehenge", "Requires the landing. Train strike crews against the railguns.", 8, 10, I["cas"], ["landing"], "has_global_flag = ac_ucw_stage_counteroffensive", "air_experience = 20", cost=3)
    f("FCU", "tango_line", "Breach the Tango Line", "Prepare the assault on Erusea's fortified lines.", 12, 10, I["defend"], ["landing"], reward="army_experience = 20", cost=3)
    f("FCU", "road_to_farbanti", "The Road to Farbanti", "Drive on the Erusean capital.", 10, 11, I["expedition"], ["strike_stonehenge", "tango_line"], war, "add_war_support = 0.05\narmy_experience = 15", cost=3)
    f("FCU", "oversee_erusea", "Oversee the Provisional Government", "Requires ISAF victory. Support Erusea's provisional government (official chronology, 26 September 2005).", 8, 12, I["diplo"], available=outcome_available("isaf_victory"), reward="add_political_power = 75\nadd_stability = 0.05", cost=3)
    f("FCU", "continental_order", "A Continental Order", "Requires the end of the war. Rebuild the treaty organization for peace. Provisional gameplay.", 12, 12, I["globe"], available=outcome_available(*OUTCOMES), reward=changes(0, -10, 10), cost=3)
    loc("ac_ucw_eru_tree", "Erusea after Ulysses")
    loc("ac_ucw_eru_tree_desc", "Erusea's path through the Ulysses fallout and the Usean Continental War, 2000–2005.")
    loc("ac_ucw_fcu_tree", "Central Usea and ISAF")
    loc("ac_ucw_fcu_tree_desc", "Central Usea's path through the Ulysses fallout and the Usean Continental War, 2000–2005.")
    for tag, tree, position in (("ERU", "ac_ucw_eru_tree", "x = 1200 y = 1700"), ("FCU", "ac_ucw_fcu_tree", "x = 1300 y = 1700")):
        OUTPUT["common/national_focus/%s.txt" % tag] = "# Authored gameplay; source: tools/build_continental_war.py.\n" + block(
            "focus_tree", "id = %s\ncountry = { factor = 0 }\ndefault = no\ncontinuous_focus_position = { %s }\n%s" % (tree, position, "\n".join(TREES[tag])))


def build_weekly():
    effect("ac_ucw_weekly", """ac_ucw_world_start = yes
ac_ucw_country_start = yes
if = {
    limit = { has_country_flag = ac_ucw_started }
    ac_ucw_fallout_tick = yes
    if = { limit = { original_tag = ERU } ac_ucw_eru_war_tick = yes }
    if = { limit = { original_tag = FCU } ac_ucw_fcu_war_tick = yes }
    ac_ucw_outcome_tick = yes
    ac_ucw_chronicle_tick = yes
    ac_ucw_assessment_tick = yes
}
ac_ucw_bound = yes""")
    OUTPUT["common/on_actions/ac_ucw.txt"] = block("on_actions", "\n".join(
        block("on_weekly_" + tag, block("effect", "ac_ucw_weekly = yes")) for tag in TAGS))


def build_playtest():
    allowed = "always = yes"
    visible = "ac_ucw_playtest_shortcuts_on = yes"
    tags = "\n".join("if = { limit = { country_exists = %s } %s = { ac_ucw_country_start = yes } }" % (tag, tag) for tag in TAGS)
    rows = [
        ("ac_playtest_ucw_open_calendar", "Playtest: open the Usean calendar", "Start the 2000–2005 Usean arc now, whatever the date. Marks Stonehenge as complete. Only for playtesting.",
         "NOT = { has_global_flag = ac_ucw_calendar_started }", "set_global_flag = ac_ucw_playtest_forced\nset_global_flag = ac_sp_stonehenge_complete\nac_ucw_world_start = yes\n" + tags),
        ("ac_playtest_ucw_raise_grievance", "Playtest: push Erusea to the brink", "Sets Erusean grievance to 80 and mobilizes its reserves, which unlocks the early invasion plan.",
         "has_global_flag = ac_ucw_calendar_started NOT = { has_global_flag = ac_ucw_war_started } country_exists = ERU", "ERU = { set_variable = { ac_ucw_grievance = 80 } set_country_flag = ac_ucw_eru_mobilized set_country_flag = ac_ucw_war_plan_ready }"),
        ("ac_playtest_ucw_start_war", "Playtest: start the Continental War", "Erusea invades San Salvacion now, as through its own decision.",
         "has_global_flag = ac_ucw_calendar_started NOT = { has_global_flag = ac_ucw_war_started } country_exists = ERU", "ERU = { ac_ucw_start_war = yes }"),
        ("ac_playtest_ucw_seize_stonehenge", "Playtest: Erusea seizes Stonehenge", "Records the seizure and its railgun spirits without moving any troops.",
         "ac_ucw_war_running = yes NOT = { has_global_flag = ac_ucw_stonehenge_seized }", "if = { limit = { ac_ucw_stonehenge_held_by_erusea = no } set_global_flag = ac_ucw_stonehenge_simulated }\nac_ucw_seize_stonehenge = yes"),
        ("ac_playtest_ucw_form_isaf", "Playtest: form ISAF", "Central Usea founds ISAF now.",
         "ac_ucw_war_running = yes NOT = { has_global_flag = ac_ucw_isaf_formed } country_exists = FCU", "FCU = { ac_ucw_form_isaf = yes }"),
        ("ac_playtest_ucw_next_stage", "Playtest: advance the war one stage", "Runs the next ISAF stage, as through its decision. Seizes Stonehenge first if the last stage needs it.",
         "ac_ucw_war_running = yes has_global_flag = ac_ucw_isaf_formed NOT = { has_global_flag = ac_ucw_stonehenge_destroyed } country_exists = FCU",
         "FCU = {\n    if = { limit = { NOT = { has_global_flag = ac_ucw_stage_los_canas } } ac_ucw_stage_los_canas = yes }\n    else_if = { limit = { NOT = { has_global_flag = ac_ucw_stage_north_point } } ac_ucw_stage_north_point = yes }\n    else_if = { limit = { NOT = { has_global_flag = ac_ucw_stage_counteroffensive } } ac_ucw_stage_counteroffensive = yes }\n    else = {\n        if = { limit = { NOT = { has_global_flag = ac_ucw_stonehenge_seized } ac_ucw_stonehenge_held_by_erusea = no } set_global_flag = ac_ucw_stonehenge_simulated }\n        ac_ucw_seize_stonehenge = yes\n        ac_ucw_stage_stonehenge = yes\n    }\n}"),
        ("ac_playtest_ucw_isaf_victory", "Playtest: force ISAF victory", "Records ISAF victory and starts the Megalith chain. The war itself is not ended.", "ac_ucw_war_running = yes", "ac_ucw_record_isaf_victory = yes"),
        ("ac_playtest_ucw_erusean_victory", "Playtest: force Erusean victory", "Records Erusean victory. The war itself is not ended.", "ac_ucw_war_running = yes", "ac_ucw_record_erusean_victory = yes"),
        ("ac_playtest_ucw_stalemate", "Playtest: force an armistice", "Erusea makes white peace with every allied participant and the war ends in a stalemate.", "ac_ucw_war_running = yes country_exists = ERU", "ERU = { ac_ucw_armistice = yes }"),
        ("ac_playtest_ucw_report", "Playtest: report the war state", "Shows the current stage, outcome and indices.", "always = yes", """if = { limit = { country_exists = ERU ERU = { has_variable = ac_ucw_grievance } } set_variable = { ac_ucw_report_grievance = ERU.ac_ucw_grievance } }
if = { limit = { country_exists = FCU FCU = { has_variable = ac_ucw_stage_weeks } } set_variable = { ac_ucw_report_weeks = FCU.ac_ucw_stage_weeks } }
country_event = { id = ac_ucw.99 days = 0 }"""),
    ]
    for ident, title, desc, available, reward in rows:
        decision("ac_playtest", ident, title, desc, available, reward, cost=0, visible=visible, single=False, ai=0, allowed=allowed, active=visible)
    event(99, "Playtest report", "Stage: [GetUcwStage]\nOutcome: [GetUcwOutcome]\nErusean grievance: [?ac_ucw_report_grievance|.0]. Weeks in the current ISAF stage: [?ac_ucw_report_weeks|.0].", [("Close the report.", "", "", 100)], picture="GFX_report_event_blank")
    loc("ac_playtest", "Playtest shortcuts")
    loc("ac_playtest_desc", "Shown only when the Playtest shortcuts game rule is enabled. Each shortcut runs the same effect as the natural route.")
    stage_texts = [("has_global_flag = ac_ucw_2005_assessed", "ac_ucw_stage_text_assessed", "The 2005 assessment has been issued"),
                   ("has_global_flag = ac_ucw_war_averted", "ac_ucw_stage_text_averted", "The war was averted"),
                   ("has_global_flag = ac_ucw_stonehenge_destroyed", "ac_ucw_stage_text_stonehenge", "Stonehenge destroyed"),
                   ("has_global_flag = ac_ucw_stage_counteroffensive", "ac_ucw_stage_text_counteroffensive", "ISAF has landed on the continent"),
                   ("has_global_flag = ac_ucw_stage_north_point", "ac_ucw_stage_text_north_point", "ISAF headquarters at North Point"),
                   ("has_global_flag = ac_ucw_stage_los_canas", "ac_ucw_stage_text_los_canas", "ISAF has fallen back to Los Canas"),
                   ("has_global_flag = ac_ucw_isaf_formed", "ac_ucw_stage_text_isaf", "ISAF has formed"),
                   ("has_global_flag = ac_ucw_war_started", "ac_ucw_stage_text_war", "The war has begun"),
                   ("has_global_flag = ac_ucw_calendar_started", "ac_ucw_stage_text_fallout", "Ulysses fallout, before the war"),
                   ("always = yes", "ac_ucw_stage_text_none", "The Usean calendar has not started")]
    outcome_texts = [("has_global_flag = ac_ucw_outcome_isaf_victory", "ac_ucw_outcome_text_isaf", "The war ended in ISAF victory."),
                     ("has_global_flag = ac_ucw_outcome_erusean_victory", "ac_ucw_outcome_text_erusea", "The war ended in Erusean victory, a provisional branch."),
                     ("has_global_flag = ac_ucw_outcome_stalemate", "ac_ucw_outcome_text_stalemate", "The war ended in an armistice, a provisional branch."),
                     ("has_global_flag = ac_ucw_war_averted", "ac_ucw_outcome_text_averted", "The war was averted, a provisional branch."),
                     ("has_global_flag = ac_ucw_war_started", "ac_ucw_outcome_text_running", "The war is still being fought."),
                     ("always = yes", "ac_ucw_outcome_text_none", "No war has been fought.")]
    texts = []
    for name, rows in (("GetUcwStage", stage_texts), ("GetUcwOutcome", outcome_texts)):
        for _, key, text in rows:
            loc(key, text)
        texts.append(block("defined_text", "name = %s\n%s" % (name, "".join(block("text", "trigger = { %s }\nlocalization_key = %s" % (cond, key)) for cond, key, _ in rows))))
    OUTPUT["common/scripted_localisation/ac_ucw.txt"] = "\n".join(texts)
    OUTPUT["common/game_rules/ac_playtest_rules.txt"] = block("ac_playtest_shortcuts", "name = ac_playtest_shortcuts_rule\ngroup = ac_economy_rule_group\n"
                                                             + block("default", "name = disabled\ntext = ac_playtest_disabled\ndesc = ac_playtest_disabled_desc")
                                                             + block("option", "name = enabled\ntext = ac_playtest_enabled\ndesc = ac_playtest_enabled_desc"))
    loc("ac_playtest_shortcuts_rule", "Playtest shortcuts")
    loc("ac_playtest_disabled", "Disabled")
    loc("ac_playtest_disabled_desc", "Normal play. No shortcut decisions are shown.")
    loc("ac_playtest_enabled", "Enabled")
    loc("ac_playtest_enabled_desc", "Shows a Playtest shortcuts decision category that can open the Usean calendar, start the Continental War and advance or end it. For testing only.")


def build_ai():
    OUTPUT["common/ai_strategy/ac_ucw.txt"] = (
        block("ac_ucw_eru_continental_war", """allowed = { original_tag = ERU }
enable = { ac_ucw_war_running = yes }
abort_when_not_enabled = yes
ai_strategy = { type = conquer id = SNS value = 200 }
ai_strategy = { type = antagonize id = FCU value = 100 }""")
        + block("ac_ucw_eru_grievance", """allowed = { original_tag = ERU }
enable = { has_country_flag = ac_ucw_started NOT = { has_global_flag = ac_ucw_war_started } check_variable = { ac_ucw_grievance > 49 } }
abort_when_not_enabled = yes
ai_strategy = { type = antagonize id = FCU value = 50 }
ai_strategy = { type = contain id = SNS value = 50 }""")
        + block("ac_ucw_fcu_isaf", """allowed = { original_tag = FCU }
enable = { ac_ucw_war_running = yes }
abort_when_not_enabled = yes
ai_strategy = { type = protect id = SNS value = 150 }
ai_strategy = { type = befriend id = NPT value = 100 }
ai_strategy = { type = antagonize id = ERU value = 100 }"""))


def build_flag_localization():
    labels = {
        "ac_ucw_calendar_started": "The Usean calendar has begun",
        "ac_ucw_playtest_forced": "The Usean calendar was opened by a playtest shortcut",
        "ac_ucw_stonehenge_operational": "Stonehenge is complete",
        "ac_ucw_refugee_closure_done": "Erusea's refugee decision has been taken",
        "ac_ucw_late_calendar": "The Usean calendar began after 2004",
        "ac_ucw_border_closed": "Erusea has closed its border",
        "ac_ucw_border_open": "Erusea has kept its border open",
        "ac_ucw_war_started": "The Usean Continental War has begun",
        "ac_ucw_war_averted": "The Usean Continental War has been averted",
        "ac_ucw_war_plan_ready": "Erusea has drawn up the San Salvacion plan",
        "ac_ucw_eru_mobilized": "Erusea's reserves are mobilized",
        "ac_ucw_isaf_prepared": "An allied charter has been drafted",
        "ac_ucw_isaf_formed": "ISAF has been founded",
        "ac_ucw_isaf_offered": "The ISAF founding has been proposed",
        "ac_ucw_stonehenge_seized": "Erusea has seized Stonehenge",
        "ac_ucw_stonehenge_destroyed": "Stonehenge has been destroyed",
        "ac_ucw_stonehenge_simulated": "Stonehenge's seizure was recorded by a playtest shortcut",
        "ac_ucw_armistice_sought": "Erusea has asked for an armistice",
        "ac_ucw_megalith_active": "Erusean officers hold Megalith",
        "ac_ucw_megalith_destroyed": "Megalith has been destroyed",
        "ac_ucw_assessment_sent": "The 2005 assessment has been issued",
        "ac_ucw_2005_assessed": "The 2005 Usean assessment has been issued",
        "ac_ucw_outcome_isaf_victory": "The war ended in ISAF victory",
        "ac_ucw_outcome_erusean_victory": "The war ended in Erusean victory",
        "ac_ucw_outcome_stalemate": "The war ended in an armistice",
        "ac_ucw_started": "The Usean brief has been opened",
        "ac_sp_stonehenge_complete": "The Stonehenge project is complete",
        "ac_npt_hosts_isaf": "North Point hosts ISAF",
        "ac_pwi_relief_strained": "The Ulysses relief effort was strained",
        "ac_pwi_relief_resilient": "The Ulysses relief effort was resilient",
    }
    for name, title, *_ in STAGES:
        labels["ac_ucw_stage_" + name] = "Completed war stage: " + title
    for flag, _, title, *_ in BRIEFS:
        labels[flag] = "Reported: " + title
        labels[flag + "_done"] = "Already past: " + title
    text = "\n".join(EFFECTS + TRIGGERS + EVENTS + [v for vs in DECISIONS.values() for v in vs] + [v for vs in TREES.values() for v in vs]
                     + [v for k, v in OUTPUT.items() if not k.endswith(".yml")])
    for key in sorted(set(re.findall(r"has_(?:country|global)_flag\s*=\s*(\w+)", text))):
        if key in LOC:
            continue
        if key.endswith("_done") and key[:-5] in LOC:
            title = "Completed: " + LOC[key[:-5]]
        elif key.endswith("_taken") and key[:-6] in LOC:
            title = "Already authorized: " + LOC[key[:-6]]
        else:
            assert key in labels, "Missing readable flag requirement: " + key
            title = labels[key]
        loc(key, title)


def render():
    build_flag_localization()
    OUTPUT["common/scripted_effects/ac_ucw.txt"] = "\n".join(EFFECTS)
    OUTPUT["common/scripted_triggers/ac_ucw.txt"] = "\n".join(TRIGGERS)
    OUTPUT["events/ac_ucw.txt"] = "\n".join(EVENTS)
    OUTPUT["common/decisions/ac_ucw.txt"] = "".join(block(category, "\n".join(rows)) for category, rows in DECISIONS.items())
    OUTPUT["localisation/english/ac_ucw_l_english.yml"] = "l_english:\n" + "\n".join(' %s:0 "%s"' % (key, text.replace('"', '\\"').replace("\n", "\\n")) for key, text in LOC.items()) + "\n"
    return OUTPUT


PROVISIONAL = "\n\n(Provisional gameplay: this branch is not part of the official chronology.)"
TEXT = {
    1: """The sky has been quiet for five months, and nobody trusts it.

Ulysses passed Earth's Roche limit on 8 July 1999 and broke apart over the world. The fragments fell for weeks. Across Usea the official counts are still being revised: towns that no longer appear on the maps, roads cut by craters, rail yards where the dispatchers work by lamplight. The worst of the impacts are behind us. The cost of them is only beginning to arrive.

The ministries have assembled the first postwar brief on [Root.GetLeader]'s desk. It is thick and contradictory. The agriculture office warns that the harvest across the continental interior will fall short for a second season. The interior office reports families walking toward any border that might take them, carrying what they could load onto carts and the roofs of buses. The treasury asks, politely, how the government means to pay for any of it.

Every capital in Usea is reading a brief like this one tonight. Some will answer it with relief convoys and credit lines, some with closed borders, and some with speeches about who is to blame. The choices made in the next three years will decide whether the continent rebuilds together or turns on itself.

Refugee pressure and fallout recovery are now tracked for our government. They are abstract measures of the strain on the state, not a record of impact sites in our provinces.""",
    10: """The border posts along the Erusean frontier were built for customs officers and the occasional smuggler. They were never meant for this.

For months the columns have come: farm families from the cratered interior, townspeople whose water supply failed, whole villages that packed up after the second wave of fragments. The camps at the crossings were meant to hold them for a few days. Some families have now been there since the autumn. The district governors send reports that grow shorter and angrier with every week: no more tents, no more flour, no more doctors willing to make the drive.

In Farbanti the cabinet meets late. The interior ministry has drafted an order to close the frontier and turn the columns back. The foreign ministry warns that the neighbours will remember it. The army reminds everyone that it is the army that would have to enforce it. Outside, the radio stations have already taken sides; one plays the order's text as if it had been signed, another reads the names of children born in the camps.

The official chronology records that Erusea stopped taking in refugees on 21 April 2000. Closing the border is that course. Keeping it open under quotas is a provisional alternative that costs recovery and eases the grievance building in our politics.""",
    11: """The trains from the north arrive full and leave empty.

Since Erusea closed its frontier, the displaced have turned toward Central Usea and its treaty partners. The first families came on foot; now they come by the hundred on requisitioned buses and fishing boats, with addresses written on scraps of paper and the names of relatives who may or may not still be alive. Reception centres in the border provinces have run out of beds. Local councils have started opening schools and sports halls without waiting for permission.

The cabinet is divided. One faction insists that the Federation's standing in Usea depends on being seen to open its doors, and that the camps can be paid for out of the reconstruction budget. Another argues that every allied capital is under the same strain, and that a treaty organization which cannot share burdens in peace will not share them in war. Both factions agree on one thing: Farbanti has chosen to make this our problem, and it has done so on purpose.""",
    12: """FARBANTI — The government of Erusea has closed its frontier to refugees, ending months of uncertainty along the continent's busiest crossings.

Border units began turning back columns at dawn. Reporters at the crossings describe lines of vehicles stretching back several kilometres, families sleeping beside their cars, and relief agencies negotiating for permission to deliver water to people who are no longer allowed to enter. The Erusean interior ministry says the closure is temporary and that the country "has carried more than its share" of the Ulysses fallout.

Neighbouring governments have reacted with alarm. Officials in Central Usea say they are preparing for a sharp increase in arrivals. Commentators across the continent are already asking the question that will shape the next three years: if Usea cannot share the burden of a disaster, what will it share instead?

The official chronology records this closure on 21 April 2000.""",
    13: """The proposal arrives through the ordinary diplomatic channels, which is itself a message.

Central Usea suggests talks: refugee quotas shared across the continent, reconstruction credit for the worst-hit Erusean districts, and a standing commission on the status of Stonehenge, the railgun battery built under the FCU's leadership to shoot down Ulysses fragments. The language is careful and generous. The Erusean foreign ministry reads it twice, looking for the condition hidden inside.

Inside the cabinet, the argument is not really about the terms. Accepting means admitting that Erusea needs help from the countries its newspapers blame for its suffering. Refusing means telling the nation that its grievances are not for sale, and leaving the camps and the craters exactly as they are. The generals have opinions. So do the families in the border towns, who have started writing to the palace.

Accepting lowers tension with the treaty powers. Refusing hardens the national mood.""" + PROVISIONAL,
    14: """Erusea has agreed to come to the table.

The delegation is small and its instructions are narrow, but it has arrived, and the first session ran past midnight. Our negotiators report that the Erusean side wants credit before quotas and recognition before either. Nobody expects a settlement this year. Still, a channel that was closed is open, and the newspapers in Farbanti have softened their headlines by a degree.

The grievance in Erusea has eased for now. It has not gone away, and the men who profit from it are still in their offices.""",
    15: """Erusea has refused our offer of talks.

The reply was short and was published in Farbanti before it reached us. It accuses the treaty powers of hoarding reconstruction credit, of building Stonehenge with continental money and then keeping it under their own control, and of lecturing a wounded country about its duties. The broadcast versions were less polite than the written one.

Our analysts read the refusal as a sign that Erusean politics now reward confrontation. That is the most dangerous kind of answer: one written for a domestic audience.""",
    20: """The first reports came from aircraft over the border: columns moving south, too many and too orderly to be refugees.

By evening the Erusean government had confirmed it. Its armies have crossed into San Salvacion, and their objective is no secret. Stonehenge, the eight-gun railgun battery built to break up Ulysses fragments before they reached the ground, stands in San Salvacion's desert. Whoever holds it holds the sky over half the continent.

The official chronology records that Erusea invaded neutral San Salvacion in the summer of 2003 and seized Stonehenge. In this campaign San Salvacion has been a member of Central Usea's treaty organization since 1991, so its partners are now being called to its defence, and the war is continental from its first day.

Radio stations across Usea have interrupted their programming. In the cities, people queue for petrol and tinned food. Many of them remember the fragments falling four years ago, and most assumed the sky had already done the worst it could do to them.

The exact start date of the war is provisional gameplay; the chronology gives only the season.""",
    25: """It was signed in a conference hall that still had tape across its cracked windows from the fragment season.

After three years of quarrels over refugees, credit and the custody of Stonehenge, Erusea and its neighbours have agreed a continental accord. Erusea renounces the use of force over the Ulysses fallout. The treaty powers commit to a shared refugee system and a reconstruction fund that Farbanti will help to administer. The railgun battery stays where it is, under an international commission with Erusean members.

Nobody in the hall pretended to like everyone else. The newspapers in every capital have found something to complain about. But the armies that were massing along the San Salvacion frontier are going back to their barracks, and the camps at the crossings are, for the first time in years, getting smaller.

In the official chronology, the Usean Continental War begins in 2003. In this campaign it has been averted.""" + PROVISIONAL,
    30: """The emergency session met in a bunker under the capital that had been built for an entirely different war.

Erusea has ignored the demand to withdraw from Stonehenge and San Salvacion. The railguns are already firing on allied aircraft, and the treaty organization's command structure, designed for peacetime exercises and parade reviews, has buckled in the first weeks. Staff officers from five countries are working out of rented offices, passing paper maps between buildings by courier.

The answer on the table is a new allied command with a single headquarters, a single chain of orders and a mandate broad enough for the war that is actually being fought. Its name has been chosen: the Independent State Allied Forces.

The official chronology records that FCU President Robert Sinclair established the ISAF on 22 August 2003. Our treaty organization will become its command.""",
    31: """The Federation of Central Usea has announced the founding of the Independent State Allied Forces, a unified allied command to drive Erusea out of San Salvacion.

The announcement was brief. It listed the member governments, named the command's mission, and declared that ISAF would accept "any nation willing to stand against aggression on this continent." Reporters noted the absence of any timetable.

In Farbanti the reaction was contempt; Erusean broadcasts called the new command a paper alliance sheltering under guns it could not reach. Along the front, allied pilots have begun painting a new insignia on their aircraft. Many of them have already flown into the range of Stonehenge, and some did not come back.

The official chronology records the ISAF's founding on 22 August 2003.""",
    32: """The invitation was delivered by hand, by an officer who had flown in under radio silence.

ISAF asks North Point to join the allied command. The island's harbours and airfields lie beyond the reach of Stonehenge's guns, and its shipyards could repair what the allies are losing on the continent. In the official chronology, ISAF moves its headquarters to North Point on 16 September 2004; the island becomes the place from which the counteroffensive is planned.

Joining would end a neutrality that North Point's government has guarded for decades. It would put the island on Erusea's target lists and its sailors on allied convoys. Declining keeps the war at a distance, for now, and leaves the allies to look elsewhere. The cabinet knows that whichever answer it gives will be remembered.

Declining is a provisional alternative to the official chronology.""",
    33: """North Point has joined the Independent State Allied Forces.

The island's government announced the decision in a short broadcast that ended with the national anthem. Within hours, allied transport aircraft were landing on its runways. Harbour authorities have begun clearing berths for warships, and dockworkers are being recalled from leave. The war has reached the island's shores, in the form of guests for now.""",
    34: """North Point has declined to join ISAF.

The reply was courteous and firm. The island's government will not join a war on the continent while its own defences are untested and its people unconsulted, but it leaves the door open: if the war turns, it says, the question can be asked again. Our staff officers have already started looking at other harbours. None of them is as good.""",
    40: """The first allied strike package to fly over the San Salvacion desert did not return intact.

Stonehenge was built to break up rock falling from orbit. Its eight railguns were designed to fire on objects travelling many times faster than any aircraft. Now Erusean crews have turned them on the sky over the battlefield, and the effect has been devastating: formations shattered at altitudes that should have been safe, squadrons forced down to treetop height where the anti-aircraft guns are waiting.

Allied air commanders have begun redrawing every flight plan on the continent around a single circle on the map. Inside it, the air belongs to Erusea.

The official chronology records that Erusea seized Stonehenge and used its railguns against aircraft.""",
    41: """The retreat has a name now, and the name is Los Canas.

ISAF's first offensive against Stonehenge has failed. The official chronology records that ISAF was pushed back to Los Canas and that its first attack on the battery failed on 14 September 2003. Allied columns are falling back along every road to the coast, covered by whatever aircraft can still fly. Supply depots that took months to fill are being burned in days so that the Erusean army cannot use them.

At Los Canas the allied command is digging in. Engineers are laying mines across the approaches, and the harbour is crowded with ships waiting to evacuate the wounded. The staff officers do not use the word "defeat" in their reports. They write about consolidation, about regrouping, and about time — the one thing the allies still have and Erusea, overstretched across a continent, does not.""",
    42: """The headquarters moved by night, in convoys of ships with their lights off.

ISAF has left the continent. Its command, its records and its surviving air wings are now based on North Point, the island nation beyond the reach of Stonehenge's guns. The official chronology records that ISAF established its headquarters in North Point on 16 September 2004.

From the island, the allied command is rebuilding: training new pilots on runways the railguns cannot touch, repairing ships in North Point's yards, and planning a return that the Erusean broadcasts insist will never come. On the continent, the occupied cities wait. Some of the people in them listen to North Point's radio station at night, with the volume turned low.""",
    43: """Before dawn, the first landing craft hit the beaches.

After a year of preparation on North Point, ISAF has returned to the Usean continent. The official chronology records that ISAF landed on 24 January 2005. Allied aircraft are flying cover from forward strips cut out of farmland. Behind the first waves come engineers, fuel bladders and the long tail of an army that intends to stay.

The Erusean command, which has spent a year holding a continent with an army built for a short war, now has to decide where to defend and what to give up. Along the occupied roads, people have started taking down the posters.""",
    44: """For the first time since the war began, allied aircraft are flying over the San Salvacion desert without dying.

ISAF has destroyed Stonehenge. The official chronology records that the battery was destroyed on 2 April 2005, with seven of its eight railguns knocked out. The strike crews who came back from the desert do not say much about it.

The weapon was built to protect Usea from Ulysses, under an international project that was meant to belong to everyone. It has ended as a ruin, after two years of being turned against the people it was built for. Allied commanders note that Erusea has lost its shield in the sky. The engineers who designed the battery are less ready to celebrate.""",
    45: """The request came through a neutral embassy, written in the formal language of surrender negotiations without using the word.

Erusea proposes an armistice along the current front lines. Its envoys say that the war has cost both sides more than either can afford, and that the continent needs reconstruction more than it needs a victor. They offer to stop where the armies stand and to talk about everything else afterwards.

Our generals are divided. Some believe Erusea is near breaking and that an armistice now would let it rebuild for another war. Others point to the casualty lists and the empty treasury. Accepting ends the war without a decision. Refusing means fighting on to the end, wherever that is.""" + PROVISIONAL,
    46: """ISAF's offer was broadcast openly, so that the Erusean people would hear it at the same time as their government.

The allied command proposes an armistice along the current front lines. The fighting would stop where the armies stand; borders, prisoners and Stonehenge would be settled at a conference afterwards. The offer is generous. It is also a test of whether the government in Farbanti can still afford to say no.

Accepting ends the war without a decision on the battlefield. Refusing commits Erusea to fighting on.""" + PROVISIONAL,
    47: """The other side has refused an armistice.

The answer came quickly enough to suggest that it had been decided before our proposal arrived. The staff officers who drafted the offer have gone back to their maps. Along the front, nobody has noticed any change at all.""",
    50: """FARBANTI — The Erusean capital has fallen, and the Usean Continental War is over.

Allied columns entered Farbanti's outskirts this week after a final offensive across the continent. The official chronology records that Farbanti fell and Erusea surrendered on 19 September 2005. Reporters describe white sheets hanging from apartment windows, Erusean soldiers stacking their rifles in the squares, and crowds that cannot decide whether to cheer or weep.

Two years after the invasion of San Salvacion, ISAF has done what its critics said it could not. The cost is still being counted: cities damaged in the fighting, a generation of pilots lost, and a continent that came through a falling sky only to tear itself apart.

Allied officers warn that the surrender has not ended every danger. Some Erusean units have not answered the order to lay down arms.""",
    51: """The broadcasts from Farbanti have been triumphant for a week.

Central Usea's command has collapsed. Its armies have capitulated or scattered, its allies are seeking terms, and Erusea's forces dominate the continent from San Salvacion to the coast. In the occupied capitals, Erusean administrators are moving into ministries whose previous occupants have fled or been arrested.

In the official chronology, ISAF wins the Continental War. In this campaign Erusea has won it, and the order that follows will be written in Farbanti.""" + PROVISIONAL,
    52: """The guns along the front have stopped, and nobody has won.

An armistice now holds between Erusea and the allied governments along the front lines as they stood on the day it was signed. Neither side has the strength to break the other, and both have agreed to stop trying, for now. Prisoners will be exchanged and commissions will meet. The maps in every staff headquarters show a line that both sides call temporary.

In the official chronology, ISAF wins the Continental War. In this campaign the war has ended in a stalemate, and the continent will have to live with a border drawn by exhaustion.""" + PROVISIONAL,
    60: """The surrender is barely a week old when the reports start coming in.

Young Erusean officers, refusing their government's order to lay down arms, have seized Megalith, a fortress built to bring down orbiting Ulysses fragments. Allied intelligence knows little about it beyond its purpose, and that purpose is enough. A weapon built to bring down fragments of Ulysses is now in the hands of men who refused to surrender.

The official chronology records that young Erusean officers seized Megalith on 26 September 2005. ISAF must take the fortress before it can be used. The pilots chosen for the mission have been told only that it may be the last flight of the war.""",
    61: """Megalith is silent.

The allied strike group went in under the fortress's defences and came out again with fewer aircraft than it took. The reports from the cockpits are fragmentary and the debriefings run long. Whatever the officers who seized it meant to do, they will not do it now.

The war is over. This time, nobody is broadcasting otherwise.""",
    62: """Erusea will govern itself again, under oversight.

The official chronology records that after Megalith was destroyed, Erusea formed a provisional autonomous government under ISAF oversight. The new administration has inherited a country with damaged cities, an army in camps and a population that lived through both a falling sky and a lost war in six years.

In this campaign the government in office remains in place. The oversight arrangement is shown as a national spirit, not a change of borders or ideology. What Erusea becomes now is a question for the years after 2005.""",
    90: """The year closes, and the archivists have started their work.

Refugee pressure stands at [?ac_ucw_pressure|.0]. Fallout recovery stands at [?ac_ucw_recovery|.0]. [GetUcwOutcome]

Six years have passed since Ulysses broke apart over the world. Usea has been shaped by the decisions taken in that time: borders opened or closed, talks accepted or refused, a war fought or averted. Some of the ministries that drafted the first fallout brief no longer exist. Many of the people who walked toward the borders in 2000 have not gone home, and some of them never will.

This is the end of the authored Usean chronology. The campaign continues; what comes next has not yet been written.""",
}
TEXT.update({
    70: """The radar station on Mount Shezna is gone.

The official chronology records that the Mount Shezna radar was destroyed on 10 October 2004, to cover ISAF's retreat from Saint Ark. With the radar silenced, the allied columns pulling back from Saint Ark had a chance to get clear. Nobody on the staff pretends it was anything but a retreat; everybody agrees it was a retreat that kept an army alive.""",
    71: """Comberth Harbor is full of burning ships.

The official chronology records that ISAF sank Erusea's Aegir fleet at Comberth Harbor on 23 November 2004. The fleet that was meant to keep the allies off the continent is gone. In the coastal towns, people watched the smoke for hours.""",
    72: """The sky over the Comona Islands was full of contrails by noon on the last day of the year.

The official chronology records a large air battle over the Comona Islands on 31 December 2004. On North Point, the staff officers planning the return to the continent read the after-action reports twice. For the first time in a long time, they were not reading about losses alone.""",
    73: """Istas Fortress has fallen, and the Tango Line is broken.

The official chronology records that ISAF took Istas Fortress and breached the Tango Line on 28 February 2005. Allied columns are moving through the gap into country that has not seen allied uniforms since the war began.""",
    74: """They came out through the desert at night, families and all.

The official chronology records that the Stonehenge engineers and their families escaped Erusean custody on 14 March 2005. The men and women who built the railguns to save the world from Ulysses are out of Erusean hands. Whatever happens to the battery now, the people who made it are safe.""",
    75: """A second front has opened in the north.

The official chronology records ISAF's northern landing at Ice Creek on 18 June 2005. The Erusean command now has to watch two fronts at once.""",
    76: """San Salvacion is free.

The official chronology records the liberation of San Salvacion on 10 July 2005. The country where the war began is the first to see it end.""",
    77: """The Whiskey Corridor has been breached.

The official chronology records that ISAF breached the Whiskey Corridor on 15 August 2005. The road toward the Erusean capital is opening.""",
})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    build_core()
    build_fallout()
    build_war()
    build_outcomes()
    build_ideas()
    build_trees()
    build_weekly()
    build_playtest()
    build_ai()
    failures = []
    for relative, text in render().items():
        path = MOD / relative
        header = "# Authored gameplay; source: tools/build_continental_war.py.\n"
        payload = text if path.suffix == ".yml" or text.startswith(header) else header + text
        encoding = "utf-8-sig" if path.suffix == ".yml" else "utf-8"
        data = payload.encode(encoding)
        if args.check:
            if not path.exists() or path.read_bytes().replace(b"\r\n", b"\n") != data:
                failures.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    if failures:
        raise SystemExit("Generated content differs: " + ", ".join(failures))
    focuses = sum(len(rows) for rows in TREES.values())
    print("Continental War: %s files, %s focuses, %s events, %s localization keys%s." % (
        len(OUTPUT), focuses, sum(1 for e in EVENTS if e.startswith(("country_event", "news_event"))), len(LOC), " checked" if args.check else " generated"))


if __name__ == "__main__":
    main()
