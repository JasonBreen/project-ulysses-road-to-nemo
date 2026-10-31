"""Generate the complete, persistent EMM/EVA campaign bundle.

The shared calendar and aid owner are built separately by build_system.py.
--check compares output bytes without editing tracked state.
"""
import argparse
import json
import sys
from pathlib import Path

from content import FOCUSES, POLICIES, policy, prep, recover

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
OUT = {}
LOC = {}


def block(key, body):
    return key + ' = {\n' + '\n'.join('\t' + line.rstrip() if line.strip() else '' for line in body.splitlines()) + '\n}\n'


def loc(key, text):
    assert key not in LOC, key
    LOC[key] = text
    return key


def once(flag, body, condition='ac_anea_active = yes'):
    return block('if', 'limit = { ' + condition + ' NOT = { has_country_flag = ' + flag + ' } }\nset_country_flag = ' + flag + '\n' + body)


def focus(row):
    loc(row.id, row.title)
    loc(row.id + '_desc', row.desc)
    available = f'original_tag = {row.tag} ac_anea_active = yes ' + row.available
    body = (f'id = {row.id}\nicon = GFX_ac_anea_focus_{row.id}\n'
            f'x = {row.x}\ny = {row.y}\ncost = {row.cost}\n')
    if row.prerequisite:
        if row.suffix == 'recovery_assessment':
            # All four recovery lanes must finish; every lane has a domestic
            # conclusion even when the bilateral accord is refused/interrupted.
            body += ''.join('prerequisite = { focus = ' + p + ' }\n' for p in row.prerequisite)
        else:
            # A single prerequisite block is OR, including the two exclusive
            # budget/distribution paths and the two aid-policy alternatives.
            body += 'prerequisite = { ' + ' '.join('focus = ' + p for p in row.prerequisite) + ' }\n'
    if row.excludes:
        body += 'mutually_exclusive = { ' + ' '.join('focus = ' + p for p in row.excludes) + ' }\n'
    body += block('available', available)
    if 'date < 1999.7.8' in row.available:
        body += block('bypass', 'has_country_flag = ac_anea_late_crisis')
    body += 'cancel_if_invalid = yes\ncontinue_if_invalid = no\n'
    body += block('ai_will_do', f'factor = {row.ai}')
    reward = row.reward
    if row.suffix == 'consultative_agency':
        reward += '\nset_country_flag = EMM_an_bureau_ready'
    body += block('completion_reward', once(row.id + '_done', reward, available))
    body += 'search_filters = { FOCUS_FILTER_POLITICAL FOCUS_FILTER_INDUSTRY }'
    return block('focus', body)


def build_trees():
    for tag, country in (('EMM', 'Emmeria'), ('EVA', 'Estovakia')):
        tree = 'ac_anea_' + tag.lower() + '_tree'
        loc(tree, country + ': The Burden of Recovery')
        loc(tree + '_desc', 'National capacity, civil protection and sustainable recovery, 1991–2005. The national policy branches are authored alternatives.')
        body = (f'id = {tree}\ncountry = {{ factor = 0 modifier = {{ add = 25 original_tag = {tag} }} }}\n'
                'default = no\ncontinuous_focus_position = { x = 50 y = 2100 }\n')
        body += '\n'.join(focus(r) for r in FOCUSES if r.tag == tag)
        OUT[f'common/national_focus/{tag}.txt'] = '# Authored Anea campaign; source: tools/anea/content.py and build_campaign.py.\n' + block('focus_tree', body)


def build_policies():
    ideas = []
    for ident, (title, desc, modifiers, kind) in POLICIES.items():
        loc(ident, title)
        loc(ident + '_desc', desc)
        ideas.append(block(ident, 'picture = ac_anea_idea_' + ident + '\nallowed = { always = no }\nallowed_civil_war = { always = no }\nremoval_cost = -1\n' + block('modifier', modifiers)))
    OUT['common/ideas/ac_anea_policies.txt'] = '# Authored gameplay policies, including their continuing opportunity costs.\n' + block('ideas', block('country', '\n'.join(ideas)))


NARRATIVE = {
 'EMM': [
  ('The Account behind the Promises',
   'The first national account is on the cabinet table. Transport officials have named the wagons that several ministries expected to use, while local authorities have listed services sustained by appropriations that were supposed to be temporary. The country has the capacity to act, but it cannot honour every promise at once. Publishing the discrepancies will invite criticism; keeping them inside the administration will leave more discretion with the officials who must resolve them. Neither course predicts the emergency that lies ahead.',
   [('Publish the account and invite local scrutiny.', 'add_political_power = -20\nadd_stability = 0.03\nset_country_flag = EMM_an_public_account', 70),
    ('Give the coordinating office authority to settle the discrepancies.', 'add_political_power = -10\nadd_stability = 0.01\nset_country_flag = EMM_an_coordinating_account', 30)]),
  ('The Cost of a Protected Allocation',
   'The budget review has reached the point where a percentage becomes a postponed repair, an unfilled training place or an official told to explain a missed deadline. Ministers can preserve the selected national priority and pay for a public review of its costs, or give the service chiefs and civil departments more room to negotiate privately. The choice does not alter the budget by itself. It determines how visibly its consequences will be recorded and how much authority the centre must spend defending them.',
   [('Fund a public review of the selected allocation.', 'add_political_power = -25\nadd_stability = 0.025\nset_country_flag = EMM_an_public_budget_review', 70),
    ('Keep the settlement within the responsible departments.', 'army_experience = 8\nadd_political_power = -10\nset_country_flag = EMM_an_departmental_budget_review', 30)]),
  ('A Warning that Must Be Explained',
   'The international warning has made uncertainty a matter of ordinary government. Local officials want to know which action they should take now, and citizens want to know why scientific assessments can change without either being dishonest. The cabinet can fund a programme of practical civil instructions, or retain more of the available attention for the readiness of the services. The latter remains a military preparation: an exercised formation is not a shelter, a medical reserve or a plan for residents without transport.',
   [('Pay for practical civil instructions and local exercises.', prep(5) + '\nadd_political_power = -20', 75),
    ('Retain the trained military liaison staff.', 'army_experience = 10\nair_experience = 5\nadd_political_power = -15', 25)]),
  ('The Shelter Work Must Be Real',
   'The revised assessment includes the eastern part of Anea, and work on the capital shelter has made emergency provision visible to the public. A building can appear complete before access, sanitation and the receiving rota are ready. The cabinet must choose whether to spend more authority testing those less visible arrangements or preserve a reserve of staff for military contingency work. The building work must be matched by people and services that can sustain those who enter.',
   [('Inspect access, sanitation and the receiving rota.', prep(7) + '\nadd_political_power = -25', 80),
    ('Preserve the military contingency staff.', 'air_experience = 10\nnavy_experience = 8\nadd_political_power = -15', 20)]),
  ('What the Preparations Preserved',
   'The reports now concern actual services, rather than estimates of future danger. Some offices can use their emergency records immediately; others are still finding the people who were supposed to maintain them. The national recovery account reflects the civil preparations completed before the crisis and Emmeria\'s comparatively resilient starting position. Ministers can keep experienced crews on immediate civilian work or release part of their time to restore service training. Neither decision changes the completed preparedness record.',
   [('Keep the crews on essential civilian work.', recover(4) + '\nadd_political_power = -20', 70),
    ('Restore the service training timetable.', 'army_experience = 12\nair_experience = 8\nadd_political_power = -15', 30)]),
  ('Assistance within the Republic\'s Means',
   'The assistance initiative for Estovakia requires cargo space, staff and receiving arrangements, not simply a declaration of sympathy. A broad mandate can keep civil contact open; a conditional mandate can defend the programme through traceable records. The cabinet must decide whether to prepare the selected policy for the bilateral accord or reserve more capacity for domestic recovery. The accord itself has a response window and requires both countries to remain eligible. An authorised service will be charged and delivered separately.',
   [('Prepare the selected assistance mandate for delivery.', 'set_country_flag = EMM_an_aid_prepared\nif = { limit = { ac_anea_can_offer = yes } ac_anea_offer_aid = yes }\nadd_political_power = -10', 80),
    ('Protect domestic capacity before authorising another service.', recover(4) + '\nset_country_flag = EMM_an_aid_restraint\nadd_political_power = -20', 20)]),
  ('The Assistance Record under Review',
   'The diplomatic review has reached an actual policy decision. The cabinet must now explain what that decision requires at home: a credible inspection capacity, a domestic reserve and records that distinguish an authorised service from delivered assistance. It can retain a standing civilian review team or release some of those specialists to the services. The review date itself does not determine whether sanctions are active; the diplomatic outcome follows the recipient\'s policy, completed monitored services and recovery record.',
   [('Keep an independent civilian review team.', 'add_political_power = -25\nadd_stability = 0.025\nset_country_flag = EMM_an_independent_review', 75),
    ('Return part of the staff to readiness work.', 'army_experience = 10\nnavy_experience = 8\nadd_political_power = -15', 25)]),
  ('An Institution or an Immediate Dividend',
   'The final recovery account has reached the cabinet after the relevant work was completed. It records civilian services, sustained defence capability and assistance actually delivered, including the cost of programmes that were refused or interrupted. A permanent recovery office would preserve skilled staff and institutional memory, while imposing a continuing claim on public administration. Releasing that capacity would bring an immediate civilian benefit but leave less standing expertise for another disruption. This assessment closes the covered national programme without predicting the next war.',
   [('Maintain a permanent recovery office.', 'add_ideas = EMM_an_recovery_office_spirit\nadd_political_power = -25\nset_country_flag = EMM_an_assessment_office', 65),
    ('Release the reserve for immediate civilian recovery.', recover(8) + '\nadd_stability = 0.025\nset_country_flag = EMM_an_assessment_dividend', 35)]),
 ],
 'EVA': [
  ('Several Countries in One Set of Returns',
   'The first reconciled account shows how far apart the reports have drifted. A workshop counted as available by one ministry is waiting for parts in another; transport promised to a district also appears in a military exercise plan. The administration can expose the contradictions and accept the political cost, or concentrate authority in a small coordinating staff. The choice will shape how shortages are explained and who has the authority to demand a correction when an official return conceals a missing service.',
   [('Publish the discrepancies and hear the districts.', 'add_political_power = -20\nadd_stability = 0.03\nset_country_flag = EVA_an_public_account', 30),
    ('Give the coordinating staff authority to reconcile them.', 'army_experience = 8\nadd_political_power = -10\nset_country_flag = EVA_an_coordinating_account', 70)]),
  ('Who Can Challenge an Allocation?',
   'The distribution register has made a political problem visible. A district can acknowledge that an order exists while still receiving none of the supplies it describes. Civil inspectors ask for the power to trace the consignment and hear an appeal. The command authorities argue that every additional signature slows urgent work. The government can fund scrutiny of its selected distribution policy, or preserve more discretion inside the responsible offices. The enduring audit or command policy remains a separate national commitment.',
   [('Pay for an accountable public complaints record.', 'add_political_power = -25\nadd_stability = 0.025\nset_country_flag = EVA_an_public_claims', 25),
    ('Retain discretion within the allocating offices.', 'army_experience = 10\nadd_stability = -0.01\nset_country_flag = EVA_an_official_discretion', 75)]),
  ('Protection before Certainty',
   'The international warning has reached the district offices before anyone can give them a complete local picture. The administration must distinguish measures that can protect civilians from promises depending on unfinished technology. It can fund practical surveys and emergency engineering, or keep more technical staff within the military readiness programme. Both have an opportunity cost. Only the civil protection work directly improves shelter access, evacuation arrangements and essential services for the public.',
   [('Fund the civil engineering and shelter surveys.', prep(5) + '\nadd_political_power = -20', 35),
    ('Preserve technical staff for command readiness.', 'army_experience = 12\nair_experience = 5\nadd_political_power = -15', 65)]),
  ('Anea Enters the Revised Estimate',
   'The revised scientific estimate includes the possibility of fragments falling in eastern Anea. District authorities need instructions based on what can actually be completed before the emergency. They ask for protected transport and engineering teams. Technical advocates also argue for preserving the personnel committed to the unfinished anti-asteroid undertaking. The government can reinforce practical civilian work or retain a record and team for future technical research. Preserving that research will not make the Chandelier operational when Ulysses arrives.',
   [('Protect district transport and civilian engineering.', prep(7) + '\nadd_political_power = -25', 30),
    ('Retain the specialist technical record and staff.', 'add_tech_bonus = { name = EVA_an_retained_research bonus = 0.5 uses = 1 category = electronics }\nadd_political_power = -20\nset_country_flag = EVA_an_retained_research', 70)]),
  ('The Returns after the Crisis',
   'District reports describe interrupted services, lost connections and repair teams without the parts they expected. The national account combines inspected district reports with the shortages confirmed by transport and utility offices. Completed civil preparedness has mitigated the initial disruption, while the unfinished strategic undertaking provides no retroactive protection. The administration can place available specialists on water and sanitation or restore military maintenance first. The decision changes the work that happens next; it cannot rewrite preparations that were never completed.',
   [('Put essential civilian services first.', recover(5) + '\nadd_political_power = -20', 35),
    ('Restore the military maintenance establishment first.', 'army_experience = 12\nair_experience = 8\nadd_stability = -0.015\nadd_political_power = -15', 65)]),
  ('The Conditions of Receiving Assistance',
   'The aid initiative has made receiving arrangements a matter of national policy. Delivery records mean little if inspectors cannot trace a consignment after it leaves the warehouse. The government can establish audited civilian distribution, paying the political cost of changing earlier practice, or keep its present allocation system and prepare a more self-reliant recovery. This choice does not answer a pending diplomatic offer on the country\'s behalf. The separate accord still requires an eligible response, and every service has its own costs and delivery checks.',
   [('Establish audited civilian distribution for the recovery programme.', policy('EVA','audited_distribution','command_distribution') + '\nadd_political_power = -35\nset_country_flag = EVA_an_recovery_audit', 20),
    ('Retain the current allocation and strengthen domestic repair.', recover(3) + '\nadd_political_power = -20\nset_country_flag = EVA_an_domestic_repair_mandate', 80)]),
  ('An Answer Based on the Actual Record',
   'The sanctions review has produced its actual diplomatic outcome. A change of language cannot replace completed monitored services, accountable distribution and restored civilian capacity. The administration must now decide whether to publish a repair timetable that can be checked or preserve more of its discretion for military readiness. The first course improves domestic recovery under either diplomatic outcome. The second keeps trained staff in the services while accepting that civilian confidence will recover more slowly.',
   [('Publish a repair timetable that can be checked.', recover(5) + '\nadd_political_power = -25\nset_country_flag = EVA_an_checkable_timetable', 35),
    ('Protect the service cadres and retain allocation discretion.', 'army_experience = 12\nair_experience = 5\nadd_stability = -0.015\nadd_political_power = -15', 65)]),
  ('What Must Survive the Emergency',
   'The concluding account is based on work completed, supplies delivered and the sustained cost of the chosen military establishment. It may record effective assistance, limited cooperation or a recovery pursued under isolation. The government can preserve a permanent civilian repair institution with a continuing administrative cost, or release its reserve into immediate reconstruction. Either decision will shape the services available to the next administration, which must inherit a usable record of the promises made and the capacity that remains.',
   [('Preserve a permanent civil repair office.', 'add_ideas = EVA_an_recovery_office_spirit\nadd_political_power = -25\nset_country_flag = EVA_an_assessment_office', 45),
    ('Use the reserve for immediate reconstruction.', recover(8) + '\nadd_stability = 0.025\nset_country_flag = EVA_an_assessment_dividend', 55)]),
 ]}


def narrative_gate(tag, index):
    if index == 1:
        return f'has_country_flag = {tag}_an_opening_ready NOT = {{ has_country_flag = ac_anea_late_init }} date < 1999.7.8'
    if index == 2:
        return f'has_country_flag = {tag}_an_allocation_ready NOT = {{ has_country_flag = ac_anea_late_init }} date < 1999.7.8'
    if index == 3:
        return 'has_country_flag = ac_anea_warning NOT = { has_country_flag = ac_anea_warning_past } NOT = { has_country_flag = ac_anea_crisis } date < 1999.7.8'
    if index == 4:
        return 'has_country_flag = ac_anea_risk_revised NOT = { has_country_flag = ac_anea_risk_revised_past } NOT = { has_country_flag = ac_anea_crisis } date < 1999.7.8' + (' date > 1998.9.19' if tag == 'EMM' else '')
    if index == 5:
        return 'has_country_flag = ac_anea_crisis NOT = { has_country_flag = ac_anea_late_crisis } date < 2000.1.10'
    if index == 6:
        return 'has_country_flag = ac_anea_crisis NOT = { has_country_flag = ac_anea_aid_past } date > 2000.1.9 date < 2002.3.20'
    if index == 7:
        return 'has_country_flag = ac_anea_crisis NOT = { has_country_flag = ac_anea_sanctions_past } has_global_flag = ac_anea_sanctions_reviewed date < 2005.12.31'
    return f'has_country_flag = {tag}_an_assessment_ready'


def build_narrative():
    loc('EVA_an_retained_research', 'Retained Technical Research')
    events = ['add_namespace = ac_anea\n']
    dispatch = []
    for tag, rows in NARRATIVE.items():
        for index, (title, desc, options) in enumerate(rows, 1):
            ident = 'ac_anea.' + str((100 if tag == 'EMM' else 200) + index)
            flag = tag + '_an_story_' + str(index)
            loc(ident + '.t', title)
            loc(ident + '.d', desc)
            gate = narrative_gate(tag, index)
            condition = f'original_tag = {tag} ac_anea_active = yes ' + gate
            body = f'id = {ident}\ntitle = {ident}.t\n'
            if index == 7:
                for outcome, prefix in [('sanctions', 'The review has imposed sanctions. '), ('alternative', 'The review has accepted an earned alternative to sanctions. '), ('lifted', 'Verified reforms have earned the lifting of previously imposed sanctions. '), ('limited', 'The review has recorded a limited or ineligible diplomatic relationship. ')]:
                    loc(ident + '.d_' + outcome, prefix + desc)
                body += block('desc', f'trigger = {{ has_global_flag = ac_anea_sanctions_active }}\ntext = {ident}.d_sanctions')
                body += block('desc', f'trigger = {{ has_global_flag = ac_anea_sanctions_avoided }}\ntext = {ident}.d_alternative')
                body += block('desc', f'trigger = {{ has_global_flag = ac_anea_sanctions_lifted }}\ntext = {ident}.d_lifted')
                body += block('desc', f'trigger = {{ NOT = {{ has_global_flag = ac_anea_sanctions_active }} NOT = {{ has_global_flag = ac_anea_sanctions_avoided }} NOT = {{ has_global_flag = ac_anea_sanctions_lifted }} }}\ntext = {ident}.d_limited')
            else:
                body += f'desc = {ident}.d\n'
            scene = 1 if index <= 2 else 2 if index <= 4 else 3 if index <= 6 else 4
            body += f'picture = GFX_ac_anea_event_{tag.lower()}_{scene}\nis_triggered_only = yes\n'
            body += block('trigger', condition + ' NOT = { has_country_flag = ' + flag + '_answered }')
            for option_index, (label, reward, ai) in enumerate(options):
                option = ident + '.' + chr(97 + option_index)
                loc(option, label)
                # Repeat the event's eligibility in the reward effect. A delayed
                # or manually repeated option cannot replay an expired reward.
                body += block('option', 'name = ' + option + '\n' + block('ai_chance', f'factor = {ai}') + once(flag + '_answered', reward, condition))
            events.append(block('country_event', body))
            dispatch.append(once(flag + '_sent', f'country_event = {{ id = {ident} days = 1 }}', condition + ' NOT = { has_country_flag = ' + flag + '_answered }'))
    OUT['events/ac_anea_narrative.txt'] = '# Authored national narratives; source: tools/anea/build_campaign.py.\n' + '\n'.join(events)
    OUT['common/scripted_effects/ac_anea_campaign.txt'] = '# Called by the shared calendar after initialization and milestone resolution.\n' + block('ac_anea_campaign_weekly', '\n'.join(dispatch))


def build_ai():
    # Priorities favour a historical policy course, rather than forcing an
    # outcome once the player has changed the causes of the sanctions review.
    for tag in ('EMM', 'EVA'):
        order = ['national_account','budget_review','civil_priority','annual_compact','workshop_register','freight_timetables','force_returns','airfield_crews','regional_desks','civil_contacts'] if tag == 'EMM' else ['national_account','allocation_review','command_distribution','district_liaisons','industrial_returns','rail_dispatch','command_returns','air_maintenance','foreign_records','technical_exchanges']
        order += ['scientific_desk' if tag == 'EMM' else 'risk_office','municipal_surveys' if tag == 'EMM' else 'district_capacity','emergency_freight' if tag == 'EMM' else 'distribution_depots','civil_account' if tag == 'EMM' else 'crisis_returns','aid_review' if tag == 'EMM' else 'aid_position','broad_assistance' if tag == 'EMM' else 'monitored_access','utility_repair' if tag == 'EMM' else 'water_recovery','sanctions_desk' if tag == 'EMM' else 'review_response','consultative_agency' if tag == 'EMM' else 'anea_delegation']
        body = ('name = ac_anea_' + tag.lower() + '_plan_name\ndesc = ac_anea_' + tag.lower() + '_plan_desc\n'
                f'allowed = {{ original_tag = {tag} }}\nenable = {{ is_historical_focus_on = yes }}\n'
                'ai_national_focuses = { ' + ' '.join(tag + '_an_' + s for s in order) + ' }\n'
                'focus_factors = { }\nresearch = { }\nideas = { }\nweight = { factor = 1 }')
        loc('ac_anea_' + tag.lower() + '_plan_name', ('Emmerian' if tag == 'EMM' else 'Estovakian') + ' recovery priorities')
        loc('ac_anea_' + tag.lower() + '_plan_desc', 'Historical policy preferences with independently evaluated aid and recovery outcomes.')
        OUT[f'common/ai_strategy_plans/{tag}_anea.txt'] = block('ac_anea_' + tag.lower() + '_historical', body)


def outputs():
    OUT.clear()
    LOC.clear()
    build_trees()
    build_policies()
    build_narrative()
    build_ai()
    OUT['localisation/english/ac_anea_campaign_l_english.yml'] = 'l_english:\n' + '\n'.join(' ' + k + ':0 ' + json.dumps(v, ensure_ascii=False) for k, v in LOC.items()) + '\n'
    return dict(OUT)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for relative, text in outputs().items():
        path = MOD / relative
        data = text.encode('utf-8-sig' if relative.endswith('.yml') else 'utf-8')
        if args.check:
            actual = path.read_bytes().replace(b'\r\n', b'\n') if path.exists() else b''
            if actual != data:
                raise SystemExit('Anea campaign output differs: ' + relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    print(f'Anea campaigns: {len(FOCUSES)} focuses, {len(POLICIES)} enduring policies, 16 substantive narratives; generated output consistent.')


if __name__ == '__main__':
    main()
