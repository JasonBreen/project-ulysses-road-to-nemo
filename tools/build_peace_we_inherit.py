"""Deterministic authoring source for The Peace We Inherit (Python 3.9+).

Run without arguments to regenerate the additive campaign files. --check is
read-only. Authored politics and coefficients are provisional gameplay; exact
primary-source chronology is recorded in docs/PEACE_WE_INHERIT.md.
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
EVENTS = ["add_namespace = ac_pwi"]
FOCUSES = []
DECISIONS = []
CABINET_CHOICES = []
TAGS = ("BLK", "OSE", "UST", "SAP", "GEB", "FAT", "REC", "SBK")
NAMES = dict(zip(TAGS, ("Belka", "Osea", "Ustio", "Sapin", "Gebet", "FATO", "Recta", "South Belka")))
FOCUS_IDS = {tag: [] for tag in TAGS}


def loc(key, text):
    assert key not in LOC, key
    LOC[key] = text


def block(key, body):
    return key + " = {\n" + "\n".join(("\t" + line).rstrip() for line in body.splitlines()) + "\n}\n"


def changes(recovery=0, confidence=0, tension=0):
    return "\n".join("add_to_variable = { ac_pwi_%s = %s }" % (name, value)
                     for name, value in (("recovery", recovery), ("confidence", confidence), ("tension", tension)) if value)


def effect(name, body):
    EFFECTS.append(block(name, body))


def once(flag, body, condition="ac_pwi_active = yes"):
    return block("if", "limit = { %s NOT = { has_country_flag = %s } }\nset_country_flag = %s\n%s\nac_pwi_bound_pressures = yes" % (condition, flag, flag, body))


def event(number, title, desc, options, trigger="always = yes", picture="GFX_report_event_treaty_2"):
    key = "ac_pwi.%d" % number
    loc(key + ".t", title)
    loc(key + ".d", desc)
    body = "id = %s\ntitle = %s.t\ndesc = %s.d\npicture = %s\nis_triggered_only = yes\ntrigger = { %s }\n" % (key, key, key, picture, trigger)
    for index, item in enumerate(options):
        label, reward, condition, weight = item
        option_key = key + "." + chr(97 + index)
        loc(option_key, label)
        if "ac_pwi_active = yes" in reward:
            # Preserve a delayed cabinet choice made during a new war; apply it
            # once peace returns instead of silently consuming the option.
            choice = "ac_pwi_choice_%s_%s" % (number, index)
            apply_choice = choice + "_apply"
            effect(apply_choice, reward)
            CABINET_CHOICES.append((choice, apply_choice))
            all_choices = " ".join("has_country_flag = ac_pwi_choice_%s_%s" % (number, i) for i in range(len(options)))
            reward = block("if", "limit = { NOT = { OR = { %s } } }\nset_country_flag = %s\n%s = yes" % (all_choices, choice, apply_choice))
        body += block("option", "name = %s\n%s\nai_chance = { factor = %s }\n%s" % (
            option_key, "trigger = { " + condition + " }" if condition else "", weight, reward))
    EVENTS.append(block("country_event", body))


def focus(tag, suffix, title, desc, x, y, prerequisite=None, available="", reward="", excludes=(), cost=5):
    ident = ("ac_pwi_" if tag == "BLK" else tag + "_pwi_") + suffix
    FOCUS_IDS[tag].append(ident)
    loc(ident, title)
    loc(ident + "_desc", desc)
    body = "id = %s\nicon = GFX_goal_generic_political_reform\nx = %s\ny = %s\ncost = %s\nai_will_do = { factor = 20 }\n" % (ident, x, y, cost)
    if prerequisite:
        body += "prerequisite = { %s }\n" % " ".join("focus = " + item for item in prerequisite)
    if excludes:
        body += "mutually_exclusive = { %s }\n" % " ".join("focus = " + item for item in excludes)
    body += "available = { original_tag = %s ac_pwi_active = yes %s }\ncancel_if_invalid = yes\ncontinue_if_invalid = no\n" % (tag, available)
    body += block("completion_reward", once(ident + "_done", reward))
    FOCUSES.append(block("shared_focus", body))
    return ident


def decision(ident, title, desc, available, reward, cost=50, visible="", cooldown=0, single=True, ai=1, active="ac_pwi_active = yes"):
    loc(ident, title)
    loc(ident + "_desc", desc)
    body = "allowed = { ac_pwi_participant = yes }\nvisible = { %s }\navailable = { %s %s }\ncost = %s\nai_will_do = { base = %s }\n" % (visible, active, available, cost, ai)
    body += "fire_only_once = %s\n" % ("yes" if single else "no")
    if cooldown:
        body += "days_re_enable = %s\n" % cooldown
    guard = active + " " + available
    if single:
        guard += " NOT = { has_country_flag = " + ident + "_taken }"
        reward = "set_country_flag = " + ident + "_taken\n" + reward
    body += block("complete_effect", block("if", "limit = { " + guard + " }\n" + reward + "\nac_pwi_bound_pressures = yes"))
    DECISIONS.append(block(ident, body))


def build_core():
    TRIGGERS.append(block("ac_pwi_participant", "OR = { " + " ".join("original_tag = " + tag for tag in TAGS) + " }"))
    TRIGGERS.append(block("ac_pwi_active", "has_country_flag = ac_pwi_started\nhas_war = no\nhas_capitulated = no"))
    effect("ac_pwi_bound_pressures", "\n".join(
        "if = { limit = { has_variable = ac_pwi_%s } clamp_variable = { var = ac_pwi_%s min = 0 max = 100 } }" % (name, name)
        for name in ("recovery", "confidence", "tension", "preparedness")))
    effect("ac_pwi_start", once("ac_pwi_started", """set_country_flag = { flag = ac_pwi_first_quarter days = 90 }
set_variable = { ac_pwi_recovery = 40 }
set_variable = { ac_pwi_confidence = 50 }
set_variable = { ac_pwi_tension = 30 }
if = {
    limit = { original_tag = BLK }
    if = { limit = { has_global_flag = ac_postwar_defeat } set_variable = { ac_pwi_recovery = 20 } set_variable = { ac_pwi_confidence = 25 } set_variable = { ac_pwi_tension = 65 } }
    else_if = { limit = { has_global_flag = ac_postwar_victory } set_variable = { ac_pwi_recovery = 45 } set_variable = { ac_pwi_confidence = 65 } set_variable = { ac_pwi_tension = 55 } }
    else_if = { limit = { has_global_flag = ac_postwar_wacht_am_wal } set_variable = { ac_pwi_recovery = 35 } set_variable = { ac_pwi_confidence = 45 } set_variable = { ac_pwi_tension = 40 } }
    else = { set_variable = { ac_pwi_recovery = 30 } set_variable = { ac_pwi_confidence = 35 } }
}
country_event = { id = ac_pwi.1 days = 1 }""", """ac_pwi_participant = yes
has_global_flag = ac_postwar_contract_started
has_war = no
has_capitulated = no
OR = { NOT = { original_tag = BLK } has_country_flag = ac_postwar_ready }"""))
    loc("ac_pwi_aftermath", "The Peace We Inherit")
    for name, title in (("recovery", "Recovery"), ("confidence", "Political confidence"), ("tension", "Settlement tension"), ("preparedness", "Preparedness"), ("relief_capacity", "Relief capacity")):
        loc("ac_pwi_" + name, title)
    loc("ac_pwi_aftermath_desc", "POSTWAR CABINET BRIEFING\nRecovery: [?ac_pwi_recovery|.0]/100. Political confidence: [?ac_pwi_confidence|.0]/100. Settlement tension: [?ac_pwi_tension|.0]/100.\nPressures change through policy and events; they do not decay every week. High tension can produce a diplomatic crisis, never an automatic new war. These indices are provisional gameplay measures.\nPreparedness: [?ac_pwi_preparedness|.0]/100. Calendar milestones continue during war; domestic reconstruction resumes when peace returns.")
    OUTPUT["common/decisions/categories/ac_pwi.txt"] = block("ac_pwi_aftermath", "priority = 60\nvisible_when_empty = yes\nallowed = { ac_pwi_participant = yes }\nvisible = { has_country_flag = ac_pwi_calendar_started }")
    event(1, "The peace we inherit", "The maps record the outcome of the war. They do not record the families waiting for news, the soldiers awaiting orders, or the ministries competing for the means to rebuild. [Root.GetLeader]'s government must publish a program it can sustain. Recovery, political confidence and settlement tension will follow the decisions taken here.", [("Open the postwar cabinet brief.", "", "", 100)])
    event(2, "Soldiers at the station", "Returning personnel bring skills that the country needs in uniform and in civilian life. Employers want hands; commanders want cadres. The government cannot promise every veteran both an immediate discharge and a permanent military post.", [
        ("Fund civilian reintegration.", once("ac_pwi_veterans_resolved", changes(10, 8, -5) + "\nadd_political_power = -25\nadd_war_support = -0.02"), "", 65),
        ("Retain an experienced training cadre.", once("ac_pwi_veterans_resolved", changes(2, 4, 8) + "\nadd_political_power = -25\narmy_experience = 10"), "", 35)])
    event(3, "Emergency powers after the emergency", "The offices established during the war still control documents, appointments and access. Civilian oversight would reassure some communities. Security officials warn that a rapid dismantling would scatter expertise. The cabinet must define an accountable mandate or accept the political cost of retaining exceptional powers.", [
        ("Require public oversight.", once("ac_pwi_emergency_resolved", changes(3, 10, -8) + "\nadd_political_power = -35"), "", 65),
        ("Retain powers under a restricted mandate.", once("ac_pwi_emergency_resolved", changes(5, 5, 7) + "\nadd_stability = 0.01"), "", 35)])
    decision("ac_pwi_repair_program", "Commission a recovery program", "Spend political capital on recovery: recovery +8, confidence +3. Available below 75 recovery, once every 180 days. If the fiscal prototype is enabled, requests its existing reconstruction policy; no separate treasury is created.", "check_variable = { ac_pwi_recovery < 75 }", changes(8, 3) + "\nif = { limit = { ac_econ_ready = yes } ac_econ_set_reconstruction = yes }", cooldown=180, single=False)
    decision("ac_pwi_public_accounts", "Publish the public accounts", "Release audited progress reports: confidence +8, tension -3. Available below 70 confidence, once every 180 days. This is political accountability, not a cash transaction.", "check_variable = { ac_pwi_confidence < 70 }", changes(0, 8, -3), cost=60, cooldown=180, single=False)
    decision("ac_pwi_deescalate", "Convene a settlement review", "Offer a public review of disputed commitments: tension -15, confidence -3, war support -2 percentage points. Available at 50 tension or higher, once every 180 days. No territory, cores or treaty obligations change automatically.", "check_variable = { ac_pwi_tension > 49 }", changes(0, -3, -15) + "\nadd_war_support = -0.02", cost=75, cooldown=180, single=False)
    decision("ac_pwi_rearm", "Retain military production capacity", "Prioritize military readiness: army experience +10, confidence +3, recovery -5, tension +10. Requires the revanchist program or a containment policy. Once every 180 days; grants no war goal.", "OR = { has_country_flag = ac_pwi_path_revanchist has_country_flag = ac_pwi_containment } check_variable = { ac_pwi_recovery > 24 }", changes(-5, 3, 10) + "\narmy_experience = 10", cooldown=180, single=False)
    event(50, "The settlement under strain", "Foreign offices are asking whether preparations announced as defensive remain compatible with the peace. [Root.GetLeader] can accept a costly review or defend the government's discretion. Neither answer settles the dispute by force.", [
        ("Pay the political cost of a review.", once("ac_pwi_tension_incident_resolved", changes(0, -5, -15) + "\nadd_political_power = -50"), "", 70),
        ("Maintain our position.", once("ac_pwi_tension_incident_resolved", changes(-5, 5, 5) + "\nadd_stability = -0.02"), "", 30)])
    event(51, "Confidence in the cabinet", "Promises have outpaced the government's capacity to deliver. The ministries propose either a public reconstruction review or a narrower program. Both leave a route back to recovery; neither can erase the cost of earlier decisions.", [
        ("Pay for a public reconstruction review.", once("ac_pwi_confidence_incident_resolved", changes(5, 15, -3) + "\nadd_political_power = -75"), "", 70),
        ("Narrow the program and defend it.", once("ac_pwi_confidence_incident_resolved", changes(3, 8, 5) + "\nadd_stability = -0.02"), "", 30)])


def build_belka():
    common = [
        ("missing", "Account for the Missing", "Open war records and prisoner inquiries. Families need an answer that can survive a change of government.", changes(3, 7)),
        ("soldiers", "Receive the Returning Soldiers", "Decide how returning personnel divide their future between civilian life and military service.", "country_event = { id = ac_pwi.2 days = 1 }"),
        ("services", "Restore Essential Services", "Restore the administrative capacity needed to deliver relief. This adds no duplicate factory or inherited reconstruction reward.", changes(10, 3)),
        ("powers", "Review the Emergency Powers", "Define what wartime institutions may retain, and to whom they must answer.", "country_event = { id = ac_pwi.3 days = 1 }"),
        ("commission", "Convene the Reconstruction Commission", "Put competing reconstruction proposals before the cabinet. Publish the costs instead of promising that every ministry can expand at once.", changes(7, 5) + "\nadd_political_power = -25"),
        ("program", "Publish the Settlement Program", "Commit the government to an initial postwar program. The institutions already governing Belka remain in place.", changes(5, 7) + "\nset_country_flag = ac_pwi_program_published"),
    ]
    previous = None
    for row, (suffix, title, desc, reward) in enumerate(common):
        previous = focus("BLK", suffix, title, desc, 30, row, [previous] if previous else ["ac_postwar_reconstruction"], reward=reward)
    branches = {
        "defeat": (24, "ac_postwar_defeat", [
            ("obligations", "Read the Settlement Obligations", "Distinguish binding inherited consequences from demands that still require negotiation.", changes(3, 3, -7)),
            ("repair", "Rebuild a Viable State", "Prioritize essential capacity over prestige projects. The peace has left a government to preserve, not an unlimited reconstruction fund.", changes(10, 4) + "\nadd_political_power = -25"),
            ("reform", "Reform the Defeated Forces", "Rebuild training and civilian oversight without erasing the inherited government or granting a new arsenal.", changes(3, 5, -5) + "\narmy_experience = 5"),
            ("neighbors", "Deal with the Victorious Powers", "Authorize talks from Belka's actual position after defeat. Any assistance still requires the other government to agree.", changes(5, 5, -5)),
        ]),
        "victory": (30, "ac_postwar_victory", [
            ("administration", "Administer the Existing Gains", "Create a workable administration for the territory the inherited peace actually transferred. Annexed Ustio is handled here; this creates no new borders or restoration.", changes(5, 4, 3) + "\nset_country_flag = ac_pwi_ustian_administration"),
            ("costs", "Publish the Cost of Occupation", "Military victory does not exempt the treasury and civil service from the cost of governing.", changes(7, -3, -5)),
            ("expectations", "Answer the Veterans' Expectations", "Recognize service without promising every veteran a permanent place in an expanding army.", changes(4, 8, -3)),
            ("dividend", "Secure a Sustainable Victory", "Choose an administration that can outlast the victory parade. This does not repeat the inherited victory-tree rewards.", changes(7, 5, -5)),
        ]),
        "wacht": (36, "ac_postwar_wacht_am_wal", [
            ("terms", "Publish the Narrow Peace", "Describe what Wacht am Wal actually achieved. A limited settlement is not a mandate for every wartime claim.", changes(3, 6, -5)),
            ("frontier", "Review the Frontier Establishment", "Balance reassurance at home against the signal sent to neighboring governments.", changes(3, 4, 5) + "\narmy_experience = 5"),
            ("recognition", "Seek Recognition of the Settlement", "Prepare reciprocal diplomacy rather than assuming recognition has already been granted.", changes(5, 4, -7)),
            ("restraint", "Make Restraint Credible", "Turn the narrower peace into a durable program without disguising it as conventional victory.", changes(7, 6, -5)),
        ]),
    }
    for outcome, (x, flag, rows) in branches.items():
        prev = "ac_pwi_program"
        for index, (suffix, title, desc, reward) in enumerate(rows):
            if index == 3:
                reward += "\nset_country_flag = ac_pwi_outcome_reviewed\ncountry_event = { id = ac_pwi.%s days = 1 }" % {"defeat": 4, "victory": 5, "wacht": 6}[outcome]
            prev = focus("BLK", outcome + "_" + suffix, title, desc, x, 6 + index, [prev], "has_global_flag = " + flag, reward)
    for number, title, text in [
        (4, "A state after defeat", "The cabinet has reviewed the obligations, recovery priorities and armed forces it inherited. The monarchy or other government already established by the existing campaign remains in office. The next decision concerns its policy, not a compulsory change of constitution."),
        (5, "A victory that must be governed", "Administration now follows the military settlement. The resources committed to governing cannot also be spent twice on domestic recovery. Belka can seek accommodation, consolidate control, or retain capacity for future confrontation."),
        (6, "A peace narrower than the slogans", "Wacht am Wal has its own balance of risks and opportunities. The government can build on restraint or interpret the settlement as temporary. Neighboring capitals will judge the program by what follows.")]:
        event(number, title, text, [("Put the postwar direction before the cabinet.", "", "", 100)])
    paths = {
        "negotiated": (24, "Negotiated Recovery", changes(8, 5, -10), "ac_pwi_accommodation", ["Civilian Oversight", "Offer Reconstruction Agreements", "Reintegrate the Wartime Institutions", "A Government of Recovery"]),
        "authoritarian": (30, "Authoritarian Consolidation", changes(5, 10, 7), "ac_pwi_central_authority", ["Centralize the Reconstruction Offices", "Define the Security Mandate", "Control the Reconstruction Program", "A Government of Order"]),
        "revanchist": (36, "Revanchist Preparation", changes(-5, 8, 12), "ac_pwi_armed_revision", ["Retain the Military Cadres", "Protect Military Production", "Challenge the Settlement Diplomatically", "A Government of Armed Revision"]),
    }
    for index, (path, (x, title, delta, idea, titles)) in enumerate(paths.items()):
        prev = "ac_pwi_program"
        for row, step_title in enumerate(titles):
            suffix = path + "_" + str(row + 1)
            reward = delta
            available = "NOT = { has_country_flag = ac_pwi_first_quarter } "
            available += "OR = { has_country_flag = ac_pwi_outcome_reviewed has_global_flag = ac_postwar_unclassified } "
            available += " ".join("NOT = { has_country_flag = ac_pwi_path_%s }" % other for other in paths if other != path)
            if path != "negotiated":
                available += " NOT = { has_global_flag = ac_postwar_unclassified }"
            if row == 0:
                reward += "\nset_country_flag = ac_pwi_path_%s\nadd_ideas = %s" % (path, idea)
            if row == 3:
                reward += "\nset_country_flag = ac_pwi_national_settlement\ncountry_event = { id = ac_pwi.%d days = 1 }" % (10 + index)
            desc = title + ": " + {
                "negotiated": "Make recovery and accountable administration the government's priority. Cooperation requires reciprocal consent; military recovery is slower.",
                "authoritarian": "Concentrate authority to deliver the program. Administrative and military benefits come with restrictions and greater foreign suspicion.",
                "revanchist": "Retain the means to challenge the peace. Readiness comes at the expense of civilian recovery and access to cooperation; this grants no war goal.",
            }[path]
            prev = focus("BLK", suffix, step_title, desc, x, 10 + row, [prev], available, reward,
                         ["ac_pwi_" + other + "_1" for other in paths if other != path] if row == 0 else ())
        event(10 + index, title + ": the national settlement", {
            "negotiated": "The government has committed itself to rebuilding through accommodation. Public oversight and international agreements offer stability, but the recovery program leaves less room for rapid military expansion.",
            "authoritarian": "The government has placed reconstruction under concentrated authority. Administrative and military institutions are more closely aligned. Restrictions at home and suspicion abroad are part of that settlement.",
            "revanchist": "The government has retained cadres and industrial capacity for a challenge to the settlement. Other capitals have reasons to be cautious. The program leaves Belka prepared for crises, without committing the country to a second war.",
        }[path], [("Carry this settlement into the coming years.", "", "", 100)])


def build_partners():
    rows = {
        "OSE": [
            ("brief", "The Cost of Peace", "Place the settlement before Congress. Osea's role depends on the outcome actually reached.", changes(3, 5), ""),
            ("accounts", "Balance Home and Overseas Commitments", "Review assistance against domestic priorities; neither budget is unlimited.", changes(6, 3) + "\nadd_political_power = -25", ""),
            ("oversight", "Review the Military Mandate", "Require civilian oversight of continued military commitments.", changes(2, 7, -3), ""),
            ("guarantor", "A Victorious Power's Responsibility", "Prepare assistance and security diplomacy from a position of victory. Other governments retain the right to refuse.", changes(5, 4, -3) + "\nset_country_flag = OSE_pwi_guarantor", "has_global_flag = ac_postwar_defeat is_subject = no"),
            ("constraints", "Recognize the Limits of Our Position", "A constrained Osea must rebuild credibility rather than assume the role of victorious guarantor.", changes(8, 5, -5), "NOT = { has_global_flag = ac_postwar_defeat }"),
            ("commitments", "Publish the Foreign Commitments", "Offer one-to-one reconstruction accords. Recognition and aid require a genuine response.", changes(3, 5) + "\nset_country_flag = OSE_pwi_diplomacy", ""),
            ("dialogue", "Keep the Settlement Open to Dialogue", "Use conditional cooperation and public scrutiny instead of military pressure.", changes(5, 4, -8) + "\nset_country_flag = ac_pwi_accommodating", ""),
            ("containment", "Prepare a Containment Policy", "Retain military capacity and challenge hostile preparations. Tension rises; no new war is scripted.", changes(-3, 6, 8) + "\nset_country_flag = ac_pwi_containment\narmy_experience = 10", ""),
        ],
        "UST": [
            ("brief", "An Ustian Postwar Administration", "Rebuild through the government and Ratio branch that survived. This does not change the country's sovereignty or focus tree.", changes(5, 5), ""),
            ("personnel", "Bring the Personnel Home", "Integrate returning soldiers and contracted specialists into accountable institutions.", changes(6, 5) + "\nadd_political_power = -25", ""),
            ("institutions", "Rebuild the Civil Administration", "Make recovery visible beyond the armed forces.", changes(8, 3), ""),
            ("sovereignty", "Negotiate as an Independent Republic", "Independent Ustio can accept assistance while retaining discretion over its security arrangements.", changes(4, 6, -5) + "\nset_country_flag = UST_pwi_independent_program", "is_subject = no"),
            ("subject", "Work Within the Surviving Administration", "A subject Ustio can rebuild domestic institutions without pretending it has independent treaty powers.", changes(7, 3), "is_subject = yes"),
            ("expertise", "Define the Role of Contracted Expertise", "Use military expertise for training, with civilian contracts and a clear command structure.", changes(3, 4, 2) + "\narmy_experience = 10", ""),
            ("security", "Review the Security Relationships", "Seek an assistance accord only when sovereignty, peace and a willing partner permit it.", changes(4, 5, -4), ""),
            ("legacy", "A State Able to Endure", "Publish a durable reconstruction and security program without erasing the surviving Ratio outcome.", changes(8, 7, -5) + "\nset_country_flag = ac_pwi_national_settlement", ""),
        ],
        "SAP": [
            ("brief", "The Government's Peace Dividend", "Put war costs before the institutions already governing Sapin. Preserve the existing balance of power and regency arrangements.", changes(4, 4), ""),
            ("costs", "Account for the War Costs", "Choose a transparent recovery program instead of concealing commitments.", changes(7, 5) + "\nadd_political_power = -25", ""),
            ("demobilize", "Negotiate Demobilization", "Manage returning soldiers without making military loyalty a substitute for political consent.", changes(6, 5, -5) + "\nadd_war_support = -0.02", ""),
            ("loyalty", "Affirm the Military Chain of Command", "Clarify the armed forces' mandate under the government actually in office.", changes(2, 7, -3), ""),
            ("commitments", "Review Foreign Commitments", "Offer reconstruction diplomacy where independence and peace permit it; acknowledge constraints where they do not.", changes(5, 4, -4), ""),
            ("legacy", "A Peace the Government Can Defend", "Carry a coherent domestic settlement into the approaching international crisis.", changes(7, 7, -5) + "\nset_country_flag = ac_pwi_national_settlement", ""),
        ],
        "GEB": [
            ("brief", "Recovery on Our Own Terms", "Inventory the government, sovereignty and industrial capacity that Gebet actually retains.", changes(5, 4), ""),
            ("industry", "Restore Industrial Coordination", "Prioritize repairs and allocation rather than receiving another free factory.", changes(9, 3) + "\nadd_political_power = -25", ""),
            ("resources", "Secure the Recovery Supply Chain", "Connect resource planning with civilian needs. This creates no new deposits or borders.", changes(7, 4), ""),
            ("security", "Review the Security Establishment", "Define what can be sustained after demobilization.", changes(3, 6, -3), ""),
            ("neighbors", "Negotiate with the Neighbors", "Independent Gebet can consider reciprocal accords. A subject administration must work within its actual authority.", changes(4, 5, -5), ""),
            ("legacy", "An Enduring Peace Dividend", "Make recovery and restrained security policy the basis of the next period.", changes(7, 7, -5) + "\nset_country_flag = ac_pwi_national_settlement", ""),
        ],
    }
    for tag, entries in rows.items():
        previous = None
        for i, (suffix, title, desc, reward, condition) in enumerate(entries):
            prerequisites = [previous] if previous else None
            x, y = 60, i
            excludes = ()
            if tag in ("OSE", "UST"):
                if i == 4:
                    prerequisites = [tag + "_pwi_" + entries[2][0]]
                    x, y = 64, 3
                elif i >= 5:
                    y = i - 1
                if i == 5:
                    prerequisites = [tag + "_pwi_" + entries[3][0], tag + "_pwi_" + entries[4][0]]
            if tag == "OSE" and i == 7:
                prerequisites = ["OSE_pwi_commitments"]
                x, y = 64, 5
                excludes = ("OSE_pwi_dialogue",)
            elif tag == "OSE" and i == 6:
                excludes = ("OSE_pwi_containment",)
            previous = focus(tag, suffix, title, desc, x, y, prerequisites, condition, reward, excludes)


PAIRS = (("BLK", "OSE"), ("OSE", "UST"), ("BLK", "GEB"), ("BLK", "SAP"), ("SAP", "OSE"), ("SAP", "GEB"))


def build_diplomacy():
    partner_checks = {tag: [] for tag in TAGS}
    for index, (sender, target) in enumerate(PAIRS):
        key = "ac_pwi_" + sender.lower() + "_" + target.lower()
        first = 100 + index * 4
        valid = "\n".join("country_exists = %s\n%s = { has_country_flag = ac_pwi_started has_war = no has_capitulated = no is_subject = no }" % (tag, tag) for tag in (sender, target))
        TRIGGERS.append(block(key + "_eligible", valid))
        TRIGGERS.append(block(key + "_answerable", "has_global_flag = %s_pending\n%s_eligible = yes\n%s = { has_country_flag = %s_window }" % (key, key, sender, key)))
        for tag in (sender, target):
            partner_checks[tag].append("AND = { has_global_flag = %s_active %s_eligible = yes }" % (key, key))
        effect(key + "_accept", block("if", "limit = { original_tag = %s %s_answerable = yes }\nclr_global_flag = %s_pending\nset_global_flag = %s_accepted\nset_global_flag = %s_active\n%s\n%s\n%s = { country_event = { id = ac_pwi.%s days = 1 } }" % (
            target, key, key, key, key,
            block(sender, changes(5, 4, -8) + "\nac_pwi_bound_pressures = yes\nadd_opinion_modifier = { target = %s modifier = ac_pwi_reconstruction_accord }" % target),
            block(target, changes(8, 5, -8) + "\nac_pwi_bound_pressures = yes\nadd_opinion_modifier = { target = %s modifier = ac_pwi_reconstruction_accord }" % sender), sender, first + 1)))
        for outcome in ("refused", "withdrawn", "timeout", "invalid"):
            effect(key + "_" + outcome, block("if", "limit = { has_global_flag = %s_pending }\nclr_global_flag = %s_pending\nset_global_flag = %s_%s\nif = { limit = { country_exists = %s } %s = { country_event = { id = ac_pwi.%s days = 1 } } }" % (key, key, key, outcome, sender, sender, first + 2)))
        effect(key + "_send", block("if", "limit = { original_tag = %s %s_eligible = yes NOT = { has_global_flag = %s_attempted } }\nset_global_flag = %s_attempted\nset_global_flag = %s_pending\nset_country_flag = { flag = %s_window days = 60 }\n%s = { country_event = { id = ac_pwi.%s days = 1 } }" % (sender, key, key, key, key, key, target, first)))
        # The country scope is fixed per dyad; no FROM saved-target assumptions.
        effect(key + "_tick", """if = {
    limit = { has_global_flag = KEY_pending }
    if = { limit = { KEY_eligible = no } KEY_invalid = yes }
    else_if = { limit = { NOT = { SENDER = { has_country_flag = KEY_window } } } KEY_timeout = yes }
}
if = {
    limit = { has_global_flag = KEY_active KEY_eligible = no }
    clr_global_flag = KEY_active
    set_global_flag = KEY_ended
    if = { limit = { country_exists = SENDER } SENDER = { remove_opinion_modifier = { target = TARGET modifier = ac_pwi_reconstruction_accord } country_event = { id = ac_pwi.END days = 1 } } }
    if = { limit = { country_exists = TARGET } TARGET = { remove_opinion_modifier = { target = SENDER modifier = ac_pwi_reconstruction_accord } } }
}""".replace("KEY", key).replace("SENDER", sender).replace("TARGET", target).replace("END", str(first + 3)))
        decision(key + "_offer", "Offer a reconstruction accord to " + NAMES[target],
                 "Authorize a reciprocal reconstruction and relief accord. The other government may accept or refuse. The offer lapses after 60 days, or if either party ceases to be independent and at peace. Acceptance improves recovery, confidence and relations for both parties. One negotiation per pair; no rewards are paid merely for sending.",
                 "%s_eligible = yes NOT = { has_global_flag = %s_attempted } NOT = { has_country_flag = ac_pwi_path_revanchist } check_variable = { ac_pwi_tension < 75 }" % (key, key),
                 key + "_send = yes", visible="original_tag = %s has_country_flag = ac_pwi_started" % sender)
        decision(key + "_withdraw", "Withdraw the reconstruction offer to " + NAMES[target],
                 "Withdraw the outstanding offer. A delayed reply cannot reactivate it or award cooperation benefits.", "%s_answerable = yes" % key, key + "_withdrawn = yes", cost=0,
                 visible="original_tag = %s has_global_flag = %s_pending" % (sender, key), ai=0)
        event(first, "A reconstruction offer from " + NAMES[sender],
              "The government of " + NAMES[sender] + " proposes reciprocal reconstruction and emergency-relief coordination. Both governments must remain independent and at peace. Acceptance supports reconstruction and improves relations; refusal leaves the domestic program intact. No territory or sovereignty is transferred.", [
                  ("Accept the accord and its administrative commitments.", key + "_accept = yes", key + "_answerable = yes", 70),
                  ("Decline, or acknowledge that the offer is no longer valid.", "if = { limit = { %s_eligible = no } %s_invalid = yes } else_if = { limit = { NOT = { %s = { has_country_flag = %s_window } } } %s_timeout = yes } else = { %s_refused = yes }" % (key, key, sender, key, key, key), "", 30)],
              trigger=key + "_answerable = yes")
        event(first + 1, "The reconstruction accord is accepted", "The other government has agreed to reciprocal coordination. The accord supports recovery and supplies a potential relief partner during the approaching crisis. Cooperation remains conditional on both countries retaining the ability to participate.", [("Record the agreement.", "", "", 100)])
        event(first + 2, "A reconstruction negotiation closes", "The negotiation has ended without an accord: it was declined, withdrawn, expired, or invalidated by changed circumstances. No assistance was booked and no recovery reward was paid. The cabinet may pursue its domestic recovery program.", [("Close the diplomatic file.", "", "", 100)])
        event(first + 3, "A relief partner can no longer participate", "War, capitulation, annexation or a change in sovereignty has made the accord inoperative. Earlier reconstruction work is not erased, but the government can no longer count this partner toward future relief capacity.", [("Update the emergency plans.", "", "", 100)])
    TRIGGERS.append(block("ac_pwi_has_relief_partner", "OR = {\n" + "\n".join(
        "AND = { original_tag = %s OR = { %s } }" % (tag, " ".join(checks))
        for tag, checks in partner_checks.items() if checks) + "\n}"))
    OUTPUT["common/opinion_modifiers/ac_pwi.txt"] = block("opinion_modifiers", block("ac_pwi_reconstruction_accord", "value = 25"))
    loc("ac_pwi_reconstruction_accord", "Reconstruction and relief accord")


def build_calendar():
    effect("ac_pwi_calendar_start", """if = {
    limit = { NOT = { has_country_flag = ac_pwi_calendar_started } }
    set_country_flag = ac_pwi_calendar_started
    set_variable = { ac_pwi_preparedness = 0 }
    set_variable = { ac_pwi_relief_capacity = 0 }
    set_variable = { ac_pwi_recovery = 0 }
    set_variable = { ac_pwi_confidence = 0 }
    set_variable = { ac_pwi_tension = 0 }
    # Old saves first loaded after a milestone record it as past, never replay it.
    if = { limit = { date > 1999.7.7 } set_country_flag = ac_pwi_warning_seen set_country_flag = ac_pwi_crisis_resolved set_country_flag = ac_pwi_late_calendar }
    if = { limit = { date > 1999.11.30 } set_country_flag = ac_pwi_assessment_done }
}""")
    TRIGGERS.append(block("ac_pwi_calendar_peace", "has_country_flag = ac_pwi_calendar_started\nhas_war = no\nhas_capitulated = no"))
    before_crisis = "date > 1996.4.19 date < 1999.7.8 NOT = { has_country_flag = ac_pwi_crisis_resolved }"
    preparation = [
        ("civil_defense", "Coordinate Civil Defense", "Prepare emergency supplies and continuity plans: preparedness +25. Commits civilian capacity for 180 days.", 25, "ac_pwi_civil_preparation", 50),
        ("logistics", "Exercise Emergency Logistics", "Practice emergency distribution: preparedness +20. Commits civilian capacity for 180 days.", 20, "ac_pwi_civil_preparation", 50),
        ("cooperate", "Coordinate with the Relief Partner", "Requires a live, accepted reconstruction accord: preparedness +25. Commits civilian capacity for 180 days; a partner lost before the crisis cannot provide the later cooperation bonus.", 25, "ac_pwi_civil_preparation", 50),
        ("readiness", "Retain Emergency Military Readiness", "Retain transport and command capacity: preparedness +10, army experience +10. Commits industrial capacity for 180 days. Competes with the civil-defense commitment through a shared 180-day capacity lock.", 10, "ac_pwi_military_preparation", 50),
    ]
    for suffix, title, desc, amount, idea, cost in preparation:
        condition = before_crisis + " NOT = { has_country_flag = ac_pwi_capacity_committed } NOT = { has_country_flag = ac_pwi_" + suffix + " }"
        if suffix == "cooperate":
            condition += " ac_pwi_has_relief_partner = yes"
        body = "set_country_flag = ac_pwi_%s\nset_country_flag = { flag = ac_pwi_capacity_committed days = 180 }\nadd_to_variable = { ac_pwi_preparedness = %s }\nadd_timed_idea = { idea = %s days = 180 }" % (suffix, amount, idea)
        if suffix == "readiness":
            body += "\narmy_experience = 10"
        decision("ac_pwi_" + suffix, title, desc, condition, body, cost=cost,
                 visible="has_country_flag = ac_pwi_calendar_started date > 1996.4.19 date < 1999.7.8", active="ac_pwi_calendar_peace = yes")
    effect("ac_pwi_resolve_ulysses", """if = {
    limit = { NOT = { has_country_flag = ac_pwi_crisis_resolved } }
    set_country_flag = ac_pwi_crisis_resolved
    set_variable = { ac_pwi_relief_capacity = ac_pwi_preparedness }
    if = { limit = { has_country_flag = ac_pwi_started check_variable = { ac_pwi_recovery > 59 } } add_to_variable = { ac_pwi_relief_capacity = 10 } }
    if = { limit = { ac_pwi_has_relief_partner = yes } add_to_variable = { ac_pwi_relief_capacity = 20 } }
    if = {
        limit = { check_variable = { ac_pwi_relief_capacity > 59 } }
        set_country_flag = ac_pwi_relief_resilient
        add_timed_idea = { idea = ac_pwi_relief_resilience days = 180 }
        if = { limit = { has_country_flag = ac_pwi_started } add_to_variable = { ac_pwi_confidence = 8 } }
    }
    else = {
        set_country_flag = ac_pwi_relief_strained
        add_timed_idea = { idea = ac_pwi_relief_strain days = 180 }
        if = { limit = { has_country_flag = ac_pwi_started } add_to_variable = { ac_pwi_confidence = -8 } }
    }
    ac_pwi_bound_pressures = yes
    country_event = { id = ac_pwi.71 days = 1 }
}""")
    # Relative settlement work and absolute world dates are deliberately separate.
    effect("ac_pwi_weekly", """ac_pwi_calendar_start = yes
ac_pwi_start = yes
ac_pwi_apply_cabinet_choices = yes
if = {
    limit = { date > 1996.4.19 date < 1999.7.8 NOT = { has_country_flag = ac_pwi_warning_seen } }
    set_country_flag = ac_pwi_warning_seen
    country_event = { id = ac_pwi.70 days = 1 }
}
if = { limit = { date > 1999.7.7 NOT = { has_country_flag = ac_pwi_crisis_resolved } } ac_pwi_resolve_ulysses = yes }
if = {
    limit = { date > 1999.11.30 NOT = { has_country_flag = ac_pwi_assessment_done } }
    set_country_flag = ac_pwi_assessment_done
    country_event = { id = ac_pwi.72 days = 1 }
}
if = {
    limit = { ac_pwi_active = yes check_variable = { ac_pwi_tension > 74 } NOT = { has_country_flag = ac_pwi_tension_incident_sent } }
    set_country_flag = ac_pwi_tension_incident_sent
    country_event = { id = ac_pwi.50 days = 1 }
}
if = {
    limit = { ac_pwi_active = yes check_variable = { ac_pwi_confidence < 25 } NOT = { has_country_flag = ac_pwi_confidence_incident_sent } }
    set_country_flag = ac_pwi_confidence_incident_sent
    country_event = { id = ac_pwi.51 days = 1 }
}
if = {
    limit = { original_tag = BLK ac_pwi_active = yes has_global_flag = ac_postwar_defeat date > 1996.1.16 date < 1997.1.1 NOT = { has_country_flag = ac_pwi_reform_briefed } }
    set_country_flag = ac_pwi_reform_briefed
    country_event = { id = ac_pwi.73 days = 1 }
}
if = {
    limit = { original_tag = BLK has_country_flag = ac_pwi_started NOT = { has_country_flag = ac_pwi_aww_observed } OR = { country_exists = AWW has_idea = BLK_awwnb_rebelion } }
    set_country_flag = ac_pwi_aww_observed
    country_event = { id = ac_pwi.74 days = 1 }
}
if = {
    limit = { original_tag = BLK ac_pwi_active = yes has_global_flag = ac_postwar_defeat date > 1997.12.31 date < 1999.1.1 NOT = { has_country_flag = ac_pwi_aggressors_briefed } }
    set_country_flag = ac_pwi_aggressors_briefed
    country_event = { id = ac_pwi.75 days = 1 }
}
if = {
    limit = { OR = { original_tag = FAT original_tag = REC original_tag = SBK } ac_pwi_active = yes NOT = { has_country_flag = ac_pwi_local_briefed } }
    set_country_flag = ac_pwi_local_briefed
    country_event = { id = ac_pwi.76 days = 1 }
}
ac_pwi_bound_pressures = yes""")
    actions = []
    for tag in TAGS:
        ticks = "\n".join("ac_pwi_%s_%s_tick = yes" % (a.lower(), b.lower()) for a, b in PAIRS if tag in (a, b))
        # Check pacts before the crisis, so invalid partners never award relief.
        actions.append(block("on_weekly_" + tag, block("effect", ticks + "\nac_pwi_weekly = yes")))
    OUTPUT["common/on_actions/ac_pwi.txt"] = block("on_actions", "\n".join(actions))
    event(70, "Ulysses: a warning for every cabinet", "The FCU has publicly announced that Ulysses will strike Earth. The announcement of 20 April 1996 is the historical reference point. Governments must now allocate capacity between civil defense, relief cooperation and military readiness. Our choices here are authored national responses, not a prediction of an impact site in our territory.", [("Open the preparedness brief.", "", "", 100)])
    event(71, "Ulysses: the relief assessment", "Ulysses passed Earth's Roche limit on 8 July 1999. This assessment concerns emergency capacity and humanitarian commitments, not invented physical damage to our provinces. Relief capacity is [?ac_pwi_relief_capacity|.0]: preparedness, effective recovery, and a partner still able to help all contribute. A capacity of 60 or more supports a resilient response; otherwise the relief effort is strained.", [("Record the demands on the emergency services.", "", "", 100)])
    event(72, "The settlement at the end of 1999", "The year closes with recovery at [?ac_pwi_recovery|.0], political confidence at [?ac_pwi_confidence|.0], and settlement tension at [?ac_pwi_tension|.0]. Preparedness reached [?ac_pwi_preparedness|.0]; assessed relief capacity was [?ac_pwi_relief_capacity|.0]. The national policy, military-readiness commitments, live accords and relief outcome remain recorded for the next period. A country still awaiting its settlement has no completed postwar program to report. The campaign continues.", [("Carry the record forward.", "set_country_flag = ac_pwi_1999_recorded", "", 100)])
    event(73, "The Belkan Air Force after defeat", "The official chronology records Waldemarr Rald's overthrow and Lieutenant General Blauvelt's air-force reformation on 17 January 1996. This briefing uses that historical reference to frame a reform debate after defeat. It does not assert that Rald still governs this campaign, appoint Blauvelt to an unsupported office, or undo the monarchy or government already established. [Root.GetLeader]'s cabinet must decide the present mandate.", [
        ("Fund accountable training institutions.", once("ac_pwi_reform_resolved", changes(4, 6, -4) + "\nadd_political_power = -25\nair_experience = 10"), "", 70),
        ("Keep the existing command arrangements.", once("ac_pwi_reform_resolved", changes(0, 3, 5) + "\nair_experience = 5"), "", 30)])
    event(74, "A World With No Boundaries: the inherited crisis", "The inherited campaign has produced A World With No Boundaries or its associated military disruption. Its historical rebellion belongs to December 1995; this campaign's existing uprising retains its own participants and consequences. The aftermath administration must account for interrupted recovery and military loyalty. This briefing does not create another rebellion or move the country to a different side.", [
        ("Publish a civilian review once peace permits.", once("ac_pwi_aww_response", changes(0, 6, -5) + "\nadd_political_power = -25"), "", 70),
        ("Preserve the records for the postwar review.", once("ac_pwi_aww_response", changes(0, 2, 3)), "", 30)])
    event(75, "Experienced pilots beyond Belka", "The official chronology records former Belkan top pilots serving abroad as aggressor instructors in 1998. The cabinet can make training and professional reintegration part of its program or keep its experienced personnel concentrated at home. These options are authored policy consequences; no named pilot is moved or given an invented biography.", [
        ("Support professional training and reintegration.", once("ac_pwi_aggressors_resolved", changes(5, 4, -5) + "\nair_experience = 5"), "", 65),
        ("Keep the training cadre at home.", once("ac_pwi_aggressors_resolved", changes(-2, 4, 5) + "\nair_experience = 10"), "", 35)])
    event(76, "A local administration after the settlement", "The inherited settlement determines the territory, government and sovereignty administered here. Our immediate choices concern recovery within that authority. An independent government may pursue its own diplomacy; a subject administration cannot promise independent guarantees. Neither option changes borders or grants sovereignty.", [
        ("Prioritize local recovery.", once("ac_pwi_local_response", changes(10, 4, -5) + "\nadd_political_power = -25"), "", 70),
        ("Retain more administrative security capacity.", once("ac_pwi_local_response", changes(4, 6, 5)), "", 30)])
    effect("ac_pwi_apply_cabinet_choices", block("if", "limit = { ac_pwi_active = yes }\n" + "\n".join(
        "if = { limit = { has_country_flag = %s } %s = yes }" % pair for pair in CABINET_CHOICES)))


def build_ideas():
    ideas = [
        ("ac_pwi_accommodation", "A Government of Recovery", "Civilian recovery and accommodation slow the pace of military expansion. Provisional gameplay policy.", "production_speed_buildings_factor = 0.05\nstability_factor = 0.03\nproduction_factory_max_efficiency_factor = -0.03"),
        ("ac_pwi_central_authority", "A Government of Order", "Central authority coordinates administration and military industry, at the cost of openness and greater suspicion. Provisional gameplay policy.", "political_power_factor = 0.05\nproduction_factory_efficiency_gain_factor = 0.05\nstability_factor = -0.03"),
        ("ac_pwi_armed_revision", "A Government of Armed Revision", "Military readiness competes with civilian recovery and foreign cooperation. This policy grants no war goal. Provisional gameplay policy.", "production_speed_arms_factory_factor = 0.08\ntraining_time_factor = -0.05\nproduction_speed_industrial_complex_factor = -0.08"),
        ("ac_pwi_civil_preparation", "Civil Capacity Committed", "Civil-defense and relief preparations temporarily divert construction capacity. Provisional gameplay cost.", "production_speed_buildings_factor = -0.05"),
        ("ac_pwi_military_preparation", "Military Capacity Committed", "Retained emergency transport and command capacity has an industrial opportunity cost. Provisional gameplay cost.", "production_factory_max_efficiency_factor = -0.05"),
        ("ac_pwi_relief_resilience", "A Resilient Relief Response", "Preparation and functioning cooperation support emergency coordination. This is humanitarian capacity, not an invented physical impact zone.", "stability_factor = 0.03\nproduction_speed_buildings_factor = 0.03"),
        ("ac_pwi_relief_strain", "Emergency Services Under Strain", "Insufficient preparation strains civilian coordination. The penalty expires; the campaign remains playable.", "stability_factor = -0.03\nproduction_speed_buildings_factor = -0.03"),
    ]
    bodies = []
    for ident, title, desc, modifiers in ideas:
        loc(ident, title)
        loc(ident + "_desc", desc)
        bodies.append(block(ident, "picture = BLK_echos_history_idea\nallowed = { always = no }\nallowed_civil_war = { always = no }\nremoval_cost = -1\n" + block("modifier", modifiers)))
    OUTPUT["common/ideas/ac_pwi.txt"] = block("ideas", block("country", "\n".join(bodies)))


def render():
    OUTPUT["common/national_focus/ac_pwi.txt"] = "\n".join(FOCUSES)
    OUTPUT["common/scripted_effects/ac_pwi.txt"] = "\n".join(EFFECTS)
    OUTPUT["common/scripted_triggers/ac_pwi.txt"] = "\n".join(TRIGGERS)
    OUTPUT["events/ac_pwi.txt"] = "\n".join(EVENTS)
    OUTPUT["common/decisions/ac_pwi.txt"] = block("ac_pwi_aftermath", "\n".join(DECISIONS))
    OUTPUT["localisation/english/ac_pwi_l_english.yml"] = "l_english:\n" + "\n".join(' %s:0 "%s"' % (key, text.replace('"', '\\"').replace("\n", "\\n")) for key, text in LOC.items()) + "\n"
    return OUTPUT


def attach_focuses():
    """Append imports inside existing trees; never replace a country tree."""
    from port_1_19.pdx import children, strip_comments_mask
    for filename, tag in (("ac_belkan_campaign.txt", "BLK"), ("OSE.txt", "OSE"), ("UST.txt", "UST"), ("SAP.txt", "SAP"), ("GEB.txt", "GEB")):
        relative = "common/national_focus/" + filename
        source = (MOD / relative).read_text(encoding="utf-8-sig")
        mask = strip_comments_mask(source)
        insertions = []
        for kind, start, end, body_start, body_end in children(source, 0, len(source), mask):
            if kind != "focus_tree":
                continue
            body = source[body_start:body_end]
            if tag == "BLK" and not re.search(r"\bid\s*=\s*ac_belkan_postwar\b", body):
                continue
            missing = [ident for ident in FOCUS_IDS[tag] if not re.search(r"\bshared_focus\s*=\s*" + re.escape(ident) + r"\b", body)]
            if missing:
                insertions.append((body_end, "\n\t# The Peace We Inherit: additive aftermath branches.\n" + "".join("\tshared_focus = " + ident + "\n" for ident in missing)))
        for position, addition in reversed(insertions):
            source = source[:position] + addition + source[position:]
        OUTPUT[relative] = source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    build_core()
    build_belka()
    build_partners()
    build_diplomacy()
    build_calendar()
    build_ideas()
    attach_focuses()
    failures = []
    for relative, text in render().items():
        path = MOD / relative
        payload = ("# Authored gameplay; source: tools/build_peace_we_inherit.py.\n" + text if path.name == "ac_pwi.txt" else text)
        encoding = "utf-8-sig" if path.suffix == ".yml" else "utf-8"
        data = payload.encode(encoding)
        if args.check:
            # Git can check text out as CRLF on Windows. Preserve BOM checking
            # while comparing authored content independently of checkout EOLs.
            if not path.exists() or path.read_bytes().replace(b"\r\n", b"\n") != data:
                failures.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    if failures:
        raise SystemExit("Generated content differs: " + ", ".join(failures))
    print("Peace We Inherit: %s files, %s focuses, %s localization keys%s." % (len(OUTPUT), len(FOCUSES), len(LOC), " checked" if args.check else " generated"))


if __name__ == "__main__":
    main()
