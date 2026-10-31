"""Generate the Anea regional owner. No engine, installed assets or fiscal writes.

--check compares bytes only. Balance is provisional gameplay; chronology and
save contracts are recorded in docs/ANEA_EXPANSION_LEDGER.md.
"""
from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / 'mod/2985041246'
OUT = {}
LOC = {}


def block(name, body):
    return name + ' = {\n' + '\n'.join('\t' + line for line in body.strip().splitlines()) + '\n}\n'


def put(path, body):
    OUT[path] = ('# Authored Anea gameplay; source: tools/anea/build_system.py.\n' + body).encode('utf-8')


def loc(key, value):
    assert key not in LOC, key
    LOC[key] = value


def guarded(condition, body):
    return block('if', 'limit = { ' + condition + ' }\n' + body)


def build():
    OUT.clear()
    LOC.clear()
    triggers = {
        'ac_anea_participant': 'OR = { original_tag = EMM original_tag = EVA }',
        'ac_anea_eligible': 'ac_anea_participant = yes has_capitulated = no',
        'ac_anea_active': 'ac_anea_eligible = yes has_country_flag = ac_anea_initialized',
        'ac_anea_pair_valid': '''country_exists = EMM country_exists = EVA
EMM = { original_tag = EMM has_capitulated = no is_subject = no NOT = { has_war_with = EVA } }
EVA = { original_tag = EVA has_capitulated = no is_subject = no }''',
        'ac_anea_offer_answerable': '''has_global_flag = ac_anea_offer_pending ac_anea_pair_valid = yes
EMM = { has_country_flag = ac_anea_offer_window }''',
        'ac_anea_can_accept': '''original_tag = EVA ac_anea_offer_answerable = yes
NOT = { has_country_flag = EVA_an_self_reliance }''',
        'ac_anea_can_offer': '''original_tag = EMM ac_anea_active = yes ac_anea_pair_valid = yes
date > 2000.1.9 date < 2000.3.11
NOT = { has_global_flag = ac_anea_offer_attempted }
NOT = { has_country_flag = ac_anea_aid_past }''',
        'ac_anea_can_serve': '''original_tag = EMM ac_anea_active = yes ac_anea_pair_valid = yes
EVA = { has_country_flag = ac_anea_initialized }
NOT = { EVA = { has_country_flag = EVA_an_self_reliance } }
OR = { NOT = { has_country_flag = EMM_an_conditional_aid } EVA = { has_country_flag = EVA_an_audited_distribution } }
has_global_flag = ac_anea_accord date > 2000.1.9 date < 2005.12.31
NOT = { has_global_flag = ac_anea_service_active }
NOT = { has_global_flag = ac_anea_aid_frozen }
NOT = { has_country_flag = ac_anea_service_cooldown }
political_power >= 25
OR = { NOT = { has_global_flag = ac_anea_sanctions_active } EVA = { has_country_flag = EVA_an_audited_distribution } }
EVA = { OR = { NOT = { has_country_flag = EVA_an_audited_distribution } political_power >= 15 } }''',
        'ac_anea_alternative_eligible': '''ac_anea_pair_valid = yes has_global_flag = ac_anea_accord
EMM = { check_variable = { ac_anea_monitored_cycles >= 2 } }
EVA = { has_country_flag = EVA_an_audited_distribution check_variable = { ac_anea_recovery >= 40 } }''',
        'ac_anea_bureau_eligible': '''original_tag = EMM ac_anea_active = yes date > 2004.1.31 date < 2005.12.31
ac_anea_pair_valid = yes has_global_flag = ac_anea_accord
NOT = { has_global_flag = ac_anea_sanctions_active }
NOT = { has_global_flag = ac_anea_bureau }''',
        'ac_anea_nec_valid': '''country_exists = NEC ac_anea_pair_valid = yes
EMM = { NOT = { has_war_with = NEC } }
EVA = { NOT = { has_war_with = NEC } }
NEC = { original_tag = NEC has_capitulated = no is_subject = no }''',
    }
    put('common/scripted_triggers/ac_anea.txt', '\n'.join(block(k, v) for k, v in triggers.items()))
    effects = {}
    effects['ac_anea_bound'] = '''clamp_variable = { var = ac_anea_preparedness min = 0 max = 100 }
clamp_variable = { var = ac_anea_recovery min = 0 max = 100 }'''
    late = ''
    for date, flag in [('1996.4.19', 'warning'), ('1998.7.28', 'risk_revised'), ('2000.3.10', 'aid'), ('2002.3.19', 'sanctions'), ('2004.1.31', 'bureau')]:
        late += guarded('date > ' + date, 'set_country_flag = ac_anea_' + flag + '_past')
    effects['ac_anea_init'] = guarded('ac_anea_participant = yes NOT = { has_country_flag = ac_anea_initialized }', '''set_country_flag = ac_anea_initialized
if = { limit = { NOT = { has_variable = ac_anea_preparedness } } set_variable = { ac_anea_preparedness = 0 } }
if = { limit = { NOT = { has_variable = ac_anea_recovery } } set_variable = { ac_anea_recovery = 0 } }
if = { limit = { original_tag = EMM NOT = { has_variable = ac_anea_monitored_cycles } } set_variable = { ac_anea_monitored_cycles = 0 } set_variable = { ac_anea_service_stage = 0 } }
''' + guarded('date > 1991.1.7', 'set_country_flag = ac_anea_late_init\n' + late + guarded('date > 1999.7.7', '''set_country_flag = ac_anea_late_crisis
set_country_flag = ac_anea_crisis
if = { limit = { original_tag = EMM } set_variable = { ac_anea_recovery = 70 } }
else = { set_variable = { ac_anea_recovery = 15 } }''')) + 'ac_anea_bound = yes')
    conversion = ''
    for tag, base, divisor, cap in [('EMM', 70, 5, 90), ('EVA', 15, 4, 40)]:
        body = 'set_variable = { ac_anea_recovery = ' + str(base) + ' }\n'
        # Threshold steps implement floor exactly using known engine primitives.
        for threshold in range(divisor, 101, divisor):
            body += guarded('check_variable = { ac_anea_preparedness > ' + str(threshold - 1) + ' }', 'add_to_variable = { ac_anea_recovery = 1 }')
        body += 'clamp_variable = { var = ac_anea_recovery min = 0 max = ' + str(cap) + ' }'
        conversion += guarded('original_tag = ' + tag, body)
    effects['ac_anea_resolve_crisis'] = guarded('ac_anea_active = yes date > 1999.7.7 NOT = { has_country_flag = ac_anea_crisis }', 'set_country_flag = ac_anea_crisis\n' + conversion + 'ac_anea_bound = yes')
    effects['ac_anea_offer_aid'] = guarded('ac_anea_can_offer = yes', '''set_global_flag = ac_anea_offer_attempted
set_global_flag = ac_anea_offer_pending
set_country_flag = { flag = ac_anea_offer_window days = 60 }
EVA = { country_event = { id = ac_anea.1 days = 1 } }''')
    effects['ac_anea_accept_aid'] = guarded('ac_anea_can_accept = yes', '''clr_global_flag = ac_anea_offer_pending
set_global_flag = ac_anea_accord
set_global_flag = ac_anea_offer_accepted
EMM = { clr_country_flag = ac_anea_offer_window }
custom_effect_tooltip = ac_anea_accord_tt''')
    effects['ac_anea_refuse_aid'] = guarded('original_tag = EVA ac_anea_offer_answerable = yes', '''clr_global_flag = ac_anea_offer_pending
set_global_flag = ac_anea_offer_refused
EMM = { clr_country_flag = ac_anea_offer_window }''')
    effects['ac_anea_close_offer'] = guarded('has_global_flag = ac_anea_offer_pending', '''clr_global_flag = ac_anea_offer_pending
if = { limit = { ac_anea_pair_valid = no } set_global_flag = ac_anea_offer_invalid }
else = { set_global_flag = ac_anea_offer_expired }
if = { limit = { country_exists = EMM } EMM = { clr_country_flag = ac_anea_offer_window } }''')
    effects['ac_anea_authorize_service'] = guarded('ac_anea_can_serve = yes', '''add_political_power = -25
set_global_flag = ac_anea_service_active
clr_global_flag = ac_anea_service_monitored
set_variable = { ac_anea_service_stage = 0 }
set_country_flag = { flag = ac_anea_delivery_due days = 60 }
add_ideas = ac_anea_relief_burden
if = {
 limit = { EVA = { has_country_flag = EVA_an_audited_distribution } }
 set_global_flag = ac_anea_service_monitored
 EVA = { add_political_power = -15 add_ideas = ac_anea_monitored_service }
}
custom_effect_tooltip = ac_anea_service_tt''')
    effects['ac_anea_end_service'] = '''clr_global_flag = ac_anea_service_active
clr_global_flag = ac_anea_service_monitored
if = { limit = { country_exists = EMM } EMM = { remove_ideas = ac_anea_relief_burden clr_country_flag = ac_anea_delivery_due set_country_flag = { flag = ac_anea_service_cooldown days = 180 } } }
if = { limit = { country_exists = EVA } EVA = { remove_ideas = ac_anea_monitored_service } }'''
    effects['ac_anea_interrupt'] = guarded('has_global_flag = ac_anea_accord ac_anea_pair_valid = no', '''clr_global_flag = ac_anea_accord
set_global_flag = ac_anea_accord_interrupted
ac_anea_end_service = yes
clr_global_flag = ac_anea_bureau
if = { limit = { country_exists = EMM } EMM = { remove_ideas = ac_anea_bureau } }
if = { limit = { country_exists = EVA } EVA = { remove_ideas = ac_anea_bureau } }
if = { limit = { country_exists = NEC } NEC = { remove_ideas = ac_anea_bureau } }''')
    effects['ac_anea_withdraw_aid'] = guarded('has_global_flag = ac_anea_accord EVA = { has_country_flag = EVA_an_self_reliance }', '''clr_global_flag = ac_anea_accord
set_global_flag = ac_anea_accord_withdrawn
ac_anea_end_service = yes''')
    effects['ac_anea_deliver'] = guarded('original_tag = EMM has_global_flag = ac_anea_service_active ac_anea_pair_valid = yes NOT = { has_country_flag = ac_anea_delivery_due }', '''if = { limit = { EVA = { NOT = { has_country_flag = EVA_an_audited_distribution } } } clr_global_flag = ac_anea_service_monitored }
if = { limit = { has_global_flag = ac_anea_service_monitored } EVA = { add_to_variable = { ac_anea_recovery = 4 } ac_anea_bound = yes } }
else = { EVA = { add_to_variable = { ac_anea_recovery = 2 } ac_anea_bound = yes } }
add_to_variable = { ac_anea_service_stage = 1 }
if = {
 limit = { check_variable = { ac_anea_service_stage > 2 } }
 if = { limit = { has_global_flag = ac_anea_service_monitored } add_to_variable = { ac_anea_monitored_cycles = 1 } }
 else = { set_global_flag = ac_anea_aid_frozen set_global_flag = ac_anea_distribution_failed }
 ac_anea_end_service = yes
}
else = { set_country_flag = { flag = ac_anea_delivery_due days = 60 } }''')
    effects['ac_anea_daily'] = '''if = { limit = { has_global_flag = ac_anea_offer_pending OR = { ac_anea_pair_valid = no EMM = { NOT = { has_country_flag = ac_anea_offer_window } } } } ac_anea_close_offer = yes }
ac_anea_interrupt = yes
ac_anea_withdraw_aid = yes
if = { limit = { has_global_flag = ac_anea_bureau OR = { NOT = { has_global_flag = ac_anea_accord } ac_anea_pair_valid = no } } clr_global_flag = ac_anea_bureau }
if = { limit = { NOT = { has_global_flag = ac_anea_service_active } }
 if = { limit = { original_tag = EMM } remove_ideas = ac_anea_relief_burden }
 if = { limit = { original_tag = EVA } remove_ideas = ac_anea_monitored_service }
}
if = { limit = { NOT = { has_global_flag = ac_anea_bureau } } remove_ideas = ac_anea_bureau }
if = { limit = { has_global_flag = ac_anea_service_active EVA = { NOT = { has_country_flag = EVA_an_audited_distribution } } } clr_global_flag = ac_anea_service_monitored }
if = { limit = { has_global_flag = ac_anea_service_active EMM = { has_country_flag = EMM_an_conditional_aid } EVA = { NOT = { has_country_flag = EVA_an_audited_distribution } } } set_global_flag = ac_anea_aid_frozen ac_anea_end_service = yes }
ac_anea_deliver = yes
if = { limit = { has_global_flag = ac_anea_nec_pending OR = { NOT = { has_global_flag = ac_anea_bureau } ac_anea_nec_valid = no EMM = { NOT = { has_country_flag = ac_anea_nec_window } } } } clr_global_flag = ac_anea_nec_pending set_global_flag = ac_anea_nec_closed }
if = { limit = { has_global_flag = ac_anea_nec_participates OR = { NOT = { has_global_flag = ac_anea_bureau } ac_anea_nec_valid = no } } clr_global_flag = ac_anea_nec_participates if = { limit = { country_exists = NEC } NEC = { remove_ideas = ac_anea_bureau } } }'''
    effects['ac_anea_review_sanctions'] = guarded('original_tag = EMM ac_anea_active = yes date > 2002.3.19 NOT = { has_global_flag = ac_anea_sanctions_reviewed } NOT = { has_country_flag = ac_anea_sanctions_past }', '''set_global_flag = ac_anea_sanctions_reviewed
if = { limit = { ac_anea_alternative_eligible = yes }
 set_global_flag = ac_anea_sanctions_avoided
 news_event = { id = ac_anea.11 days = 1 }
}
else_if = { limit = { ac_anea_pair_valid = yes }
 set_global_flag = ac_anea_sanctions_active
 EVA = { add_ideas = ac_anea_sanctions }
 news_event = { id = ac_anea.10 days = 1 }
}
else = { set_global_flag = ac_anea_sanctions_unavailable }''')
    effects['ac_anea_reconsider_sanctions'] = guarded('original_tag = EMM ac_anea_active = yes has_global_flag = ac_anea_sanctions_active ac_anea_alternative_eligible = yes', '''clr_global_flag = ac_anea_sanctions_active
set_global_flag = ac_anea_sanctions_lifted
EVA = { remove_ideas = ac_anea_sanctions }
news_event = { id = ac_anea.12 days = 1 }''')
    effects['ac_anea_resume_aid'] = guarded('original_tag = EMM ac_anea_active = yes ac_anea_pair_valid = yes has_global_flag = ac_anea_accord has_global_flag = ac_anea_aid_frozen EVA = { has_country_flag = EVA_an_audited_distribution } political_power >= 25', '''add_political_power = -25
clr_global_flag = ac_anea_aid_frozen
set_global_flag = ac_anea_aid_reformed''')
    effects['ac_anea_found_bureau'] = guarded('ac_anea_bureau_eligible = yes', '''set_global_flag = ac_anea_bureau
add_ideas = ac_anea_bureau
EVA = { add_ideas = ac_anea_bureau }
if = { limit = { ac_anea_nec_valid = yes NOT = { has_global_flag = ac_anea_nec_attempted } }
 set_global_flag = ac_anea_nec_attempted set_global_flag = ac_anea_nec_pending
 set_country_flag = { flag = ac_anea_nec_window days = 60 }
 NEC = { country_event = { id = ac_anea.20 days = 1 } }
}''')
    effects['ac_anea_accept_nec'] = guarded('original_tag = NEC ac_anea_nec_valid = yes has_global_flag = ac_anea_bureau has_global_flag = ac_anea_nec_pending EMM = { has_country_flag = ac_anea_nec_window }', '''clr_global_flag = ac_anea_nec_pending
set_global_flag = ac_anea_nec_participates
add_ideas = ac_anea_bureau''')
    effects['ac_anea_refuse_nec'] = guarded('original_tag = NEC has_global_flag = ac_anea_nec_pending', 'clr_global_flag = ac_anea_nec_pending\nset_global_flag = ac_anea_nec_closed')
    effects['ac_anea_calendar'] = '''if = { limit = { ac_anea_active = yes }
 if = { limit = { date > 1996.4.19 } set_country_flag = ac_anea_warning }
 if = { limit = { date > 1998.7.28 } set_country_flag = ac_anea_risk_revised }
 ac_anea_resolve_crisis = yes
 if = { limit = { original_tag = EMM }
  ac_anea_review_sanctions = yes
  if = { limit = { is_ai = yes ac_anea_can_offer = yes } ac_anea_offer_aid = yes }
  if = { limit = { is_ai = yes ac_anea_can_serve = yes } ac_anea_authorize_service = yes }
  if = { limit = { is_ai = yes ac_anea_bureau_eligible = yes } ac_anea_found_bureau = yes }
 }
}'''
    effects['ac_anea_weekly'] = '''ac_anea_init = yes
ac_anea_calendar = yes
ac_anea_campaign_weekly = yes
ac_anea_bound = yes'''
    for kind, condition, reward, cooldown in [
        ('prepare', 'ac_anea_active = yes date < 1999.7.8 political_power >= 25 NOT = { has_country_flag = ac_anea_prepare_cooldown }', 'add_political_power = -25\nadd_to_variable = { ac_anea_preparedness = 3 }', 180),
        ('repair', 'ac_anea_active = yes has_country_flag = ac_anea_crisis political_power >= 35 NOT = { has_country_flag = ac_anea_repair_cooldown }', 'add_political_power = -35\nadd_to_variable = { ac_anea_recovery = 4 }', 180),
        ('train', 'ac_anea_active = yes political_power >= 25 NOT = { has_country_flag = ac_anea_train_cooldown }', 'add_political_power = -25\narmy_experience = 6\nair_experience = 3', 180),
    ]:
        triggers['ac_anea_can_' + kind] = condition + ' NOT = { has_country_flag = ac_anea_domestic_allocation }'
        effects['ac_anea_' + kind] = guarded('ac_anea_can_' + kind + ' = yes', reward + '\nset_country_flag = { flag = ac_anea_domestic_allocation days = 180 }\nset_country_flag = { flag = ac_anea_' + kind + '_cooldown days = ' + str(cooldown) + ' }\nadd_timed_idea = { idea = ac_anea_domestic_works days = 180 }\nac_anea_bound = yes')
    put('common/scripted_triggers/ac_anea.txt', '\n'.join(block(k, v) for k, v in triggers.items()))
    put('common/scripted_effects/ac_anea.txt', '\n'.join(block(k, v) for k, v in effects.items()))
    weekly = '\n'.join(block('on_weekly_' + tag, block('effect', 'ac_anea_weekly = yes')) for tag in ('EMM', 'EVA'))
    startup = block('on_startup', block('effect', 'EMM = { ac_anea_init = yes }\nEVA = { ac_anea_init = yes }'))
    daily = ''.join(block('on_daily_' + tag, block('effect', 'ac_anea_daily = yes')) for tag in ('EMM', 'EVA', 'NEC'))
    put('common/on_actions/ac_anea.txt', block('on_actions', startup + weekly + daily))
    build_events()
    build_decisions()
    build_ideas()
    put('common/scripted_localisation/ac_anea.txt', '\n'.join(block('defined_text', 'name = ' + name + '\n' + '\n'.join(block('text', ('trigger = { ' + trigger + ' }\n' if trigger else '') + 'localization_key = ' + key) for trigger, key in choices)) for name, choices in {
        'GetAneaAccordStatus': [('has_global_flag = ac_anea_aid_frozen', 'ac_anea_status_frozen'), ('has_global_flag = ac_anea_accord', 'ac_anea_status_live'), ('has_global_flag = ac_anea_offer_pending', 'ac_anea_status_pending'), ('', 'ac_anea_status_none')],
        'GetAneaSanctionsStatus': [('has_global_flag = ac_anea_sanctions_active', 'ac_anea_status_sanctions'), ('has_global_flag = ac_anea_sanctions_avoided', 'ac_anea_status_alternative'), ('has_global_flag = ac_anea_sanctions_lifted', 'ac_anea_status_lifted'), ('', 'ac_anea_status_review')],
    }.items()))
    for key, value in {'ac_anea_status_frozen': 'Suspended: distribution reform is required.', 'ac_anea_status_live': 'Accepted and eligible for renewed service.', 'ac_anea_status_pending': 'Awaiting a reply within the 60-day window.', 'ac_anea_status_none': 'No active bilateral accord.', 'ac_anea_status_sanctions': 'Sanctions active.', 'ac_anea_status_alternative': 'Monitored cooperation chosen at the review.', 'ac_anea_status_lifted': 'Sanctions lifted after verified reform.', 'ac_anea_status_review': 'No current sanctions decision.', 'ac_anea_accord_tt': 'The accord permits separately funded 180-day services. Acceptance grants no equipment or recovery by itself.', 'ac_anea_service_tt': 'Pay the authorisation costs once. Deliveries occur after 60, 120 and 180 days, subject to continued eligibility. Completed aid is retained if the service is interrupted.'}.items(): loc(key, value)
    OUT['localisation/english/ac_anea_system_l_english.yml'] = ('l_english:\n' + '\n'.join(' ' + key + ':0 "' + value.replace('"', '\\"').replace('\n', '\\n') + '"' for key, value in LOC.items()) + '\n').encode('utf-8-sig')


def build_events():
    events = ['add_namespace = ac_anea']
    def event(number, title, desc, options, trigger='', news=False):
        key = 'ac_anea.' + str(number)
        loc(key + '.t', title);loc(key + '.d', desc)
        body = f'id = {key}\ntitle = {key}.t\ndesc = {key}.d\npicture = GFX_ac_anea_event_emm_4\nis_triggered_only = yes\n'
        if trigger: body += block('trigger', trigger)
        for index, (label, condition, effect, weight) in enumerate(options):
            option = key + '.' + chr(97 + index);loc(option, label)
            body += block('option', 'name = ' + option + '\n' + (block('trigger', condition) if condition else '') + block('ai_chance', 'factor = ' + str(weight)) + effect)
        events.append(block('news_event' if news else 'country_event', body))
    event(1, 'An Emmerian Relief Accord', 'Emmeria proposes a standing civilian relief accord. Every service period will require a fresh allocation, and the recipient must choose who controls distribution. The founding offer expires after sixty days; its acceptance does not deliver supplies on its own.', [
        ('Accept the accord and its separate service authorisations.', 'ac_anea_can_accept = yes', 'ac_anea_accept_aid = yes', 80),
        ('Rely on domestic recovery.', 'ac_anea_offer_answerable = yes', 'ac_anea_refuse_aid = yes', 20),
        ('Record that the offer is no longer actionable.', 'ac_anea_offer_answerable = no', 'ac_anea_close_offer = yes', 100),
    ], 'original_tag = EVA')
    for number, title, desc in [
        (10, 'Anean Reconstruction Sanctions', 'The reconstruction review has ended in sanctions. Diversion, administrative failures and incomplete verified deliveries have prevented an agreed alternative. Humanitarian services may resume under monitored distribution, and a later review can recognise actual reform.'),
        (11, 'An Alternative to Sanctions', 'Two monitored relief services and an audited distribution system have given the reconstruction review a different outcome. Cooperation will continue under the live accord. This is an earned campaign alternative to the historical sanctions course.'),
        (12, 'Verified Reform Changes the Review', 'The record now includes audited distribution, two completed monitored services and sufficient civilian recovery. Sanctions have been lifted. The earlier review remains part of the national record; completed costs and aid are not replayed.'),
    ]: event(number, title, desc, [('Record the actual outcome.', '', '', 100)], news=True)
    event(20, 'An Anean Consultative Bureau', 'Emmeria and Estovakia have opened a civilian bureau for technical information and relief logistics. Nordennavic is invited to participate without a change of government, border or military alignment. A refusal leaves the bilateral bureau in place.', [
        ('Participate in civilian coordination.', 'ac_anea_nec_valid = yes has_global_flag = ac_anea_nec_pending EMM = { has_country_flag = ac_anea_nec_window }', 'ac_anea_accept_nec = yes', 60),
        ('Keep our existing arrangements.', '', 'ac_anea_refuse_nec = yes', 40),
    ], 'original_tag = NEC')
    put('events/ac_anea.txt', '\n'.join(events))


def build_decisions():
    cats = []
    decisions = []
    recovery = []
    relief = []
    def decision(ident, title, desc, condition, effect, tag='', visible='', weight=1):
        loc(ident, title);loc(ident + '_desc', desc)
        return block(ident,
            'icon = ac_anea_' + ('relief' if tag else 'recovery') + '\nallowed = { ' + ('original_tag = ' + tag if tag else 'ac_anea_participant = yes') + ' }\n' +
            block('visible', visible or ('ac_anea_active = yes')) + block('available', condition) +
            'cost = 0\nfire_only_once = no\ndays_re_enable = 7\n' + block('ai_will_do', 'base = ' + str(weight)) + block('complete_effect', effect))
    for kind, title, desc in [
        ('prepare', 'Exercise Civil Protection', 'Commit 25 political power and 180 days of civilian construction attention to gain 3 preparedness. This is a shelter, evacuation and emergency-supply exercise; it expires before the crisis.'),
        ('repair', 'Fund a Domestic Repair Programme', 'Commit 35 political power and 180 days of civilian construction attention to gain 4 recovery. Domestic repair remains useful if aid is refused, suspended or interrupted.'),
        ('train', 'Protect Readiness Training', 'Commit 25 political power and 180 days of civilian construction attention to gain 6 army experience and 3 air experience. Training does not increase civil preparedness.'),
    ]: recovery.append(decision('ac_anea_' + kind + '_decision', title, desc, 'ac_anea_can_' + kind + ' = yes', 'ac_anea_' + kind + ' = yes'))
    for tag in ('EMM', 'EVA'):
        recovery.append(decision(tag + '_an_enter_campaign', 'Enter the Anean Campaign', 'After the current generic focus is finished, adopt the new national campaign while retaining completed content. No starting army, industry, technology or historical preparation rewards are granted.',
            'ac_anea_active = yes ac_anea_generic_idle = yes',
            guarded('original_tag = ' + tag + ' ac_anea_active = yes ac_anea_generic_idle = yes NOT = { has_focus_tree = ac_anea_' + tag.lower() + '_tree }', 'load_focus_tree = { tree = ac_anea_' + tag.lower() + '_tree keep_completed = yes }'),
            tag=tag, visible='ac_anea_active = yes NOT = { has_focus_tree = ac_anea_' + tag.lower() + '_tree }', weight=0))
    for ident, title, desc, condition, effect, visible in [
        ('offer', 'Propose the Relief Accord', 'Send the once-only founding offer. Estovakia has sixty days to respond. Separate service authorisations pay for actual assistance.', 'ac_anea_can_offer = yes', 'ac_anea_offer_aid = yes', 'date > 2000.1.9 date < 2000.3.11 NOT = { has_global_flag = ac_anea_offer_attempted }'),
        ('serve', 'Authorise a Relief Service', 'Pay 25 political power and carry a 1% consumer-goods burden for 180 days. Monitored participation also costs Estovakia 15 political power. Three deliveries give 4 recovery each under monitoring, or 2 each under command distribution. Completion is followed by a 180-day cooldown.', 'ac_anea_can_serve = yes', 'ac_anea_authorize_service = yes', 'has_global_flag = ac_anea_accord'),
        ('resume', 'Reopen Aid under Audited Distribution', 'Pay 25 political power to reopen the suspended accord after Estovakia adopts audited distribution. Service authorisation remains a separate payment.', 'has_global_flag = ac_anea_aid_frozen ac_anea_pair_valid = yes EVA = { has_country_flag = EVA_an_audited_distribution } political_power >= 25', 'ac_anea_resume_aid = yes', 'has_global_flag = ac_anea_accord has_global_flag = ac_anea_aid_frozen'),
        ('review', 'Recognise Verified Reconstruction Reform', 'Lift active sanctions after audited distribution, two completed monitored services, recovery of at least 40 and a still-valid accord. This does not undo the earlier review or replay rewards.', 'has_global_flag = ac_anea_sanctions_active ac_anea_alternative_eligible = yes', 'ac_anea_reconsider_sanctions = yes', 'has_global_flag = ac_anea_sanctions_active'),
        ('bureau', 'Open the Anean Consultative Bureau', 'Coordinate civilian information and relief logistics with Estovakia. Invite Nordennavic where eligible. This creates no common state, military alliance or forced integration.', 'ac_anea_bureau_eligible = yes', 'ac_anea_found_bureau = yes', 'date > 2004.1.31 NOT = { has_global_flag = ac_anea_bureau }'),
    ]: relief.append(decision('ac_anea_' + ident + '_decision', title, desc, 'ac_anea_active = yes ' + condition, effect, tag='EMM', visible='ac_anea_active = yes ' + visible))
    for name, icon, rows in [('ac_anea_recovery', 'recovery', recovery), ('ac_anea_relief', 'relief', relief)]:
        cats.append(block(name, 'icon = ac_anea_' + icon + '\nallowed = { ac_anea_participant = yes }\nvisible = { ac_anea_active = yes }'))
        decisions.append(block(name, '\n'.join(rows)))
    loc('ac_anea_recovery', 'Anea: Civil Protection and Recovery')
    loc('ac_anea_recovery_desc', 'Preparedness: [?ac_anea_preparedness|0]/100. Recovery: [?ac_anea_recovery|0]/100.\n\nCivil protection changes the crisis starting position. Domestic repair restores civilian capacity. Readiness training protects military skills at an opportunity cost. These are provisional campaign measures.')
    loc('ac_anea_relief', 'Anea: Aid and Regional Cooperation')
    loc('ac_anea_relief_desc', '[GetAneaAccordStatus]\n[GetAneaSanctionsStatus]\n\nCurrent service deliveries: [?EMM.ac_anea_service_stage|0]/3. Completed monitored services: [?EMM.ac_anea_monitored_cycles|0].\n\nAn alternative to sanctions requires audited Estovakian distribution, two completed monitored services, recovery of at least 40 and a valid accord. Each service and cooldown lasts 180 days.')
    put('common/decisions/categories/ac_anea.txt', '\n'.join(cats))
    put('common/decisions/ac_anea.txt', '\n'.join(decisions))
    # Use shipped focus_progress syntax, not the tutorial-only
    # has_set_nat_focus token. An explicit opt-in also avoids automatic swaps.
    sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
    from script import parse, walk, get
    ids = []
    for source in [MOD / 'common/national_focus/generic.txt', *sorted((MOD / 'common/continuous_focus').glob('*.txt'))]:
        ids += [get(n, 'id') for k, n in walk(parse(source.read_text(encoding='utf-8-sig'))) if k == 'focus']
    idle = '\n'.join('NOT = { AND = { NOT = { has_completed_focus = ' + ident + ' } OR = { has_shine_effect_on_focus = ' + ident + ' focus_progress = { focus = ' + ident + ' progress > 0 } } } }' for ident in ids)
    path = 'common/scripted_triggers/ac_anea.txt'
    OUT[path] += ('\n' + block('ac_anea_generic_idle', idle)).encode()


def build_ideas():
    rows = []
    for name, title, desc, modifier in [
        ('relief_burden', 'Anean Relief Allocation', 'A funded 180-day relief service reserves civilian production. Paid allocations and completed deliveries persist if cooperation ends.', 'consumer_goods_factor = 0.01'),
        ('monitored_service', 'Monitored Relief Administration', 'Civil administrators maintain audited distribution during the service. Their political allocation was paid at authorisation.', 'political_power_gain = -0.05'),
        ('sanctions', 'Reconstruction Sanctions', 'Restrictions following the reconstruction review impede imports and industrial recovery. Verified reform can earn reconsideration.', 'production_speed_industrial_complex_factor = -0.05 production_factory_max_efficiency_factor = -0.03'),
        ('bureau', 'Anean Civilian Consultation', 'Civilian technical and logistics coordination improves rebuilding. This office carries no military or constitutional integration.', 'production_speed_infrastructure_factor = 0.04'),
        ('domestic_works', 'Competing National Allocations', 'The current civil-protection, repair or training allocation ties up some civilian construction attention for 180 days.', 'production_speed_industrial_complex_factor = -0.02'),
    ]:
        ident = 'ac_anea_' + name;loc(ident, title);loc(ident + '_desc', desc)
        rows.append(block(ident, 'picture = ' + ident + '\nallowed = { always = no }\nremoval_cost = -1\n' + block('modifier', modifier)))
    put('common/ideas/ac_anea.txt', block('ideas', block('country', '\n'.join(rows))))


def main():
    parser = argparse.ArgumentParser();parser.add_argument('--check', action='store_true');args = parser.parse_args()
    build()
    different = []
    for relative, data in OUT.items():
        path = MOD / relative
        if args.check:
            if not path.exists() or path.read_bytes().replace(b'\r\n', b'\n') != data: different.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True);path.write_bytes(data)
    if different: raise SystemExit('Anea system output differs: ' + ', '.join(different))
    print('Anea regional owner:', len(OUT), 'files; generated output matches' if args.check else 'files generated')


if __name__ == '__main__': main()
