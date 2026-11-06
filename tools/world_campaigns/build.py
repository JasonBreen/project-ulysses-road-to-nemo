"""Compile complete original national programme contracts; --check is read-only."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
from content import CAST, COUNTRIES, SOURCE

OUT = {}
LOC = {}
ROWS = []
MODIFIERS = {
    'civil': [('stability_factor', .03), ('production_speed_buildings_factor', .03), ('planning_speed', .04)],
    'industry': [('production_factory_max_efficiency_factor', .03), ('production_factory_efficiency_gain_factor', .04), ('industrial_capacity_factory', .03)],
    'logistics': [('supply_consumption_factor', -.03), ('production_speed_infrastructure_factor', .04), ('army_org_factor', .03)],
    'air': [('air_accidents_factor', -.05), ('air_mission_efficiency', .03), ('air_agility_factor', .02)],
    'land': [('army_defence_factor', .03), ('training_time_army_factor', -.04), ('planning_speed', .04)],
    'naval': [('convoy_escort_efficiency', .04), ('naval_detection', .03), ('naval_coordination', .03)],
    'intelligence': [('research_speed_factor', .02), ('production_factory_efficiency_gain_factor', .03), ('planning_speed', .03)],
    'research': [('research_speed_factor', .02), ('production_factory_efficiency_gain_factor', .03), ('army_org_factor', .02)],
    'diplomacy': [('stability_factor', .02), ('production_speed_buildings_factor', .02), ('army_org_factor', .02)],
}


def block(key, body):
    return key + ' = {\n' + ''.join('\t' + line + '\n' for line in body.splitlines()) + '}\n'


def guard(condition, body):
    return block('if', block('limit', condition) + body)


def loc(key, text):
    if key in LOC and LOC[key] != text:
        raise ValueError('Conflicting localization: ' + key)
    LOC[key] = text
    return key


def flag(key, text):
    loc(key, text)
    loc(key + '_desc', text + '.')
    return key


def emit(path, text):
    OUT[path] = ('# Original fiction/provisional gameplay; owner: tools/world_campaigns/build.py\n' + text).encode()


def active(tag):
    return f'tag = {tag} original_tag = {tag} has_capitulated = no any_owned_state = {{ is_controlled_by = PREV }}'


def common():
    loc('ac_wc_active_tt', 'The original national government controls territory and can administer this programme')
    loc('ac_wc_budget_tt', 'The fiscal owner can pay 0.02 billion without arrears, or the disabled/legacy fiscal rule is selected')
    loc('ac_wc_payment_tt', 'Reserve 25 political power and, in the full fiscal model, pay 0.02 billion for a 90-day operation. Interrupted work retains its paid costs and can be attempted again.')
    loc('ac_wc_fiction_tt', 'Original campaign fiction and provisional gameplay; this programme does not assert official history.')
    for state, text in [('paid', 'The fiscal owner accepted the operation payment'), ('running', 'The funded operation is in progress'), ('failed', 'The operation was interrupted; no completion reward was granted')]:
        flag('ac_wc_' + state, text)
    budget = ('OR = { AND = { ac_macro_ready = yes check_variable = { ac_macro_arrears = 0 } '
              'check_variable = { ac_macro_cash >= 0.02 } } '
              'has_game_rule = { rule = ac_economy option = disabled } '
              'has_game_rule = { rule = ac_economy option = experimental } }')
    triggers = block('ac_wc_can_pay', block('custom_trigger_tooltip', 'tooltip = ac_wc_budget_tt\n' + budget))
    effects = block('ac_wc_pay', 'clr_country_flag = ac_wc_paid\n' + guard('ac_macro_ready = yes',
        'set_temp_variable = { ac_macro_transaction_amount = 0.02 }\nac_macro_try_spend = yes\n' + guard('has_country_flag = ac_macro_transaction_succeeded', 'set_country_flag = ac_wc_paid')) +
        guard('OR = { has_game_rule = { rule = ac_economy option = disabled } has_game_rule = { rule = ac_economy option = experimental } }', 'set_country_flag = ac_wc_paid'))
    for tag in COUNTRIES:
        triggers += block('ac_wc_' + tag.lower() + '_active', block('custom_trigger_tooltip', 'tooltip = ac_wc_active_tt\n' + active(tag)))
    emit('common/scripted_triggers/ac_wc_programmes.txt', triggers)
    emit('common/scripted_effects/ac_wc_programmes.txt', effects)


def country(tag, chapters):
    stem = 'ac_wc_' + tag.lower()
    namespace = stem
    focuses, effects, events, decisions, ideas = [], [], [], [], []
    loc(stem + '_tree', 'Sotoa: The Republic We Choose' if tag == 'SOA' else 'Central Sotoa: Our Own Voice')
    loc(stem + '_tree_desc', 'An original national campaign of governing mandates, practical development and reciprocal diplomacy. Programme choices are provisional gameplay, not official earlier history.')
    loc(stem + '_programmes', 'National Programme Operations')
    loc(stem + '_programmes_desc', 'A focus opens a specific national problem. Its dialogue selects a programme; the operation then needs a separate payment and 90 days of uninterrupted administration. A completed programme supports a renewable, bounded national service. These are original campaign stories and provisional gameplay.')
    profile = json.loads((ROOT / 'tools/world_foundation/country_registry.json').read_text())
    original = next(row for row in profile['countries'] if row['tag'] == tag)
    for policy, titles in enumerate(chapters[0].paths):
        ident = f'{tag}_wc_government_{policy}'
        loc(ident, titles[0])
        loc(ident+'_desc', 'The enduring founding mandate selected in this original national campaign. It changes administrative priorities, not the inherited ruling party, leader or constitutional history. Ordinary sector services do not replace this mandate.')
        modifier = ('stability_factor = 0.02\nplanning_speed = -0.02' if policy == 0 else
                    'industrial_capacity_factory = 0.02\nstability_factor = -0.01' if policy == 1 else
                    'army_org_factor = 0.02\nstability_factor = -0.01')
        ideas.append(block(ident, f'picture = {tag}_wc_civil\nallowed = {{ always = no }}\nremoval_cost = -1\n'+block('modifier',modifier)))
    for domain, modifiers in MODIFIERS.items():
        for policy, (modifier, value) in enumerate(modifiers):
            ident = tag + '_wc_' + domain + '_' + str(policy)
            loc(ident, ('Civil' if policy == 0 else 'Technical' if policy == 1 else 'Service') + ' ' + domain.title() + ' Programme')
            loc(ident + '_desc', 'A funded national service, renewable after its term. Its benefit occupies civilian political attention. Different approaches in this sector replace one another; they do not stack. Original fiction and provisional balance.')
            ideas.append(block(ident, 'picture = ' + tag + '_wc_' + domain + '\nallowed = { always = no }\nremoval_cost = -1\n' + block('modifier', f'{modifier} = {value}\npolitical_power_gain = -0.02')))
    for index, chapter in enumerate(chapters):
        key = f'{tag}_wc_e1_{chapter.slug}'
        started = flag(key + '_opened', chapter.title + ': the national discussion has opened')
        pending = flag(key + '_pending', chapter.title + ': a programme choice is pending')
        running = flag(key + '_running', chapter.title + ': paid work is underway')
        maturing = flag(key + '_maturing', chapter.title + ': the 90-day operation term has not elapsed')
        done = flag(key + '_done', chapter.title + ': the operation was completed')
        completed = flag(key + '_completed', chapter.title + ': the final focus was completed')
        failed = flag(key + '_failed', chapter.title + ': the previous attempt was interrupted')
        service = flag(key + '_service_term', chapter.title + ': the funded service term has not expired')
        choices = [flag(key + '_choice_' + str(i), chapter.paths[i][0] + ' was selected') for i in range(3)]
        unavailable = ' '.join('NOT = { has_country_flag = ' + f + ' }' for f in choices)
        event_id = namespace + '.' + str(index + 1)
        root_id = key + '_open'
        x, y = (index % 3) * 8 + 2, (index // 3) * 6
        root_reward = guard(f'ac_wc_{tag.lower()}_active = yes NOT = {{ has_country_flag = {started} }}',
                            f'set_country_flag = {started}\nset_country_flag = {{ flag = {pending} days = 60 }}\ncountry_event = {{ id = {event_id} days = 1 }}')
        founding = '' if index == 0 else block('prerequisite', '\n'.join(
            f'focus = {tag}_wc_e1_{chapters[0].slug}_p{i}_2' for i in range(3)))
        add_focus(focuses, tag, chapter, root_id, chapter.title, x, y, founding, root_reward,
                  'The opening dialogue chooses one of three programmes. No operation is completed or paid merely by opening the discussion.')
        event_options = ''
        for policy, titles in enumerate(chapter.paths):
            p = f'{key}_p{policy}'
            choice = choices[policy]
            option_valid = f'ac_wc_{tag.lower()}_active = yes has_country_flag = {pending} {unavailable}'
            event_options += block('option', 'name = ' + loc(event_id + '.p' + str(policy), titles[0]) + '\n' +
                block('trigger', option_valid) +
                block('ai_chance', 'factor = ' + str((50, 35, 15)[policy])) +
                guard(option_valid, f'clr_country_flag = {pending}\nset_country_flag = {choice}\ncustom_effect_tooltip = ac_wc_fiction_tt'))
            prior = root_id
            for stage, title in enumerate(titles):
                ident = p + '_' + str(stage)
                prereq = f'prerequisite = {{ focus = {prior} }}\n'
                if stage == 0:
                    prereq += block('mutually_exclusive', '\n'.join('focus = ' + f'{key}_p{other}_0' for other in range(3) if other != policy))
                condition = f'has_country_flag = {choice}' + (f' has_country_flag = {done}' if stage == 2 else '')
                receipt = flag(ident + '_receipt', title + ' completed')
                body = f'set_country_flag = {receipt}\n'
                if stage == 0:
                    body += 'custom_effect_tooltip = ac_wc_fiction_tt\n'
                elif stage == 1:
                    # Experience is a bounded preparatory effect, never equipment.
                    body += ('air_experience = 2' if chapter.domain == 'air' else 'navy_experience = 2' if chapter.domain == 'naval' else 'army_experience = 2' if chapter.domain == 'land' else 'add_political_power = 2') + '\n'
                else:
                    body += f'set_country_flag = {completed}\nset_country_flag = {{ flag = {service} days = 365 }}\n' + apply_service(tag, chapter.domain, policy)
                    if index == 0:
                        route = flag(f'{tag}_wc_route_{policy}', titles[0] + ': founding mandate adopted')
                        body += f'set_country_flag = {route}\nadd_ideas = {tag}_wc_government_{policy}\n'
                body = guard(f'ac_wc_{tag.lower()}_active = yes NOT = {{ has_country_flag = {receipt} }} {condition}', body)
                explanation = ('Authorize the programme; the separate paid operation is still required.' if stage == 0 else
                               'Prepare the staff and procedures. Preparation is not an equipment or industrial grant.' if stage == 1 else
                               'Requires the actual paid operation result. Establish a 365-day service; other approaches in this sector are replaced. Continuing renewal remains a paid decision.')
                add_focus(focuses, tag, chapter, ident, title, x + (policy - 1) * 2, y + stage + 1,
                          prereq, body, explanation, condition)
                prior = ident
        events.append(block('country_event', f'id = {event_id}\ntitle = {loc(event_id+".t", chapter.title)}\ndesc = {loc(event_id+".d", chapter.problem + "\\n\\n" + " / ".join(n + ", " + r for n, r in CAST[tag]) + ". This is an original campaign discussion, not an official historical event.")}\npicture = GFX_{tag}_wc_scene_{chapter.domain}\nis_triggered_only = yes\n' + event_options +
            block('option', 'name = ' + loc(event_id + '.defer', 'Return the proposal to the staff') + '\n' +
                  block('trigger', f'OR = {{ ac_wc_{tag.lower()}_active = no NOT = {{ has_country_flag = {pending} }} }}') + f'clr_country_flag = {pending}')))
        reopen = guard(f'ac_wc_{tag.lower()}_active = yes {unavailable} NOT = {{ has_country_flag = {pending} }}',
                       f'set_country_flag = {{ flag = {pending} days = 60 }}\ncountry_event = {{ id = {event_id} days = 1 }}')
        decisions.append(decision(key + '_reopen', 'Reopen: ' + chapter.title,
            'Resume the unanswered dialogue. No preparation, payment or reward is replayed.',
            f'ac_wc_{tag.lower()}_active = yes has_country_flag = {started} {unavailable}',
            f'NOT = {{ has_country_flag = {pending} }}', reopen, cost=0))
        selected = 'OR = { ' + ' '.join('has_country_flag = ' + f for f in choices) + ' }'
        ready = 'OR = { ' + ' '.join('has_completed_focus = ' + f'{key}_p{i}_1' for i in range(3)) + ' }'
        valid = f'ac_wc_{tag.lower()}_active = yes {selected} {ready}'
        finish = guard(valid + f' has_country_flag = {running} NOT = {{ has_country_flag = {maturing} }} NOT = {{ has_country_flag = {done} }}',
                       f'set_country_flag = {done}\nclr_country_flag = {running}\nclr_country_flag = {failed}')
        finish += guard(f'has_country_flag = {running}', f'clr_country_flag = {running}\nset_country_flag = {failed}')
        payment = 'ac_wc_pay = yes\n' + guard('has_country_flag = ac_wc_paid',
                   f'set_country_flag = {running}\nset_country_flag = {{ flag = {maturing} days = 90 }}\nclr_country_flag = {failed}')
        op = decision(key + '_operate', 'Fund: ' + chapter.title,
            'Pay 25 political power and, when the full fiscal owner is ready, 0.02 billion. Carry out the selected programme for 90 days. Territory loss or capitulation interrupts the work without a completion reward. Paid costs are retained; retry remains available. This operation grants no factories, units or equipment.',
            f'ac_wc_{tag.lower()}_active = yes {ready} NOT = {{ has_country_flag = {done} }}',
            f'ac_wc_can_pay = yes NOT = {{ has_country_flag = {running} }}',
            guard(valid + f' ac_wc_can_pay = yes NOT = {{ has_country_flag = {running} }} NOT = {{ has_country_flag = {done} }}', payment),
            extra='days_remove = 90\nremove_effect = {\n' + finish + '}\n' +
                  block('cancel_trigger', f'ac_wc_{tag.lower()}_active = no') +
                  block('cancel_effect', f'clr_country_flag = {running}\nset_country_flag = {failed}'))
        decisions.append(op)
        renew = ''
        for policy in range(3):
            renew += guard(f'has_country_flag = {choices[policy]}', apply_service(tag, chapter.domain, policy))
        decisions.append(decision(key + '_renew', 'Renew: ' + chapter.title,
            'Renew the chosen service for 365 days. Pay 25 political power and, with a full ready fiscal account, 0.02 billion. Sector approaches replace one another rather than stacking. Renewal does not replay the focus or grant equipment.',
            f'ac_wc_{tag.lower()}_active = yes has_country_flag = {completed}', f'ac_wc_can_pay = yes NOT = {{ has_country_flag = {service} }}',
            guard(f'ac_wc_{tag.lower()}_active = yes ac_wc_can_pay = yes NOT = {{ has_country_flag = {service} }}',
                'ac_wc_pay = yes\n' + guard('has_country_flag = ac_wc_paid', f'set_country_flag = {{ flag = {service} days = 365 }}\n' + renew)), cooldown=365))
        ROWS.append(dict(tag=tag, era='e1', chapter=chapter.slug, title=chapter.title, domain=chapter.domain,
            source_layer='approved original fiction / provisional gameplay', reference=SOURCE,
            focuses=[root_id] + [f'{key}_p{p}_{s}' for p in range(3) for s in range(3)],
            event=event_id, operation=key+'_operate', cast=CAST[tag],
            inherited_states=original['owned_states'], state_changes=False, native_acceptance=False))
    tree = f'id = {stem}_tree\ncountry = {{ factor = 0 modifier = {{ add = 80 tag = {tag} original_tag = {tag} }} }}\ndefault = no\nreset_on_civilwar = no\ncontinuous_focus_position = {{ x = 2600 y = 16 }}\ninitial_show_position = {{ focus = {tag}_wc_e1_{chapters[0].slug}_open }}\n' + ''.join(focuses)
    emit('common/national_focus/' + stem + '.txt', block('focus_tree', tree))
    emit('events/' + stem + '.txt', 'add_namespace = ' + namespace + '\n' + ''.join(events))
    emit('common/ideas/' + stem + '.txt', block('ideas', block('country', ''.join(ideas))))
    emit('common/decisions/categories/' + stem + '.txt', block(stem + '_programmes',
        f'icon = {tag}_wc_civil\nallowed = {{ tag = {tag} original_tag = {tag} }}\nvisible = {{ ac_wc_{tag.lower()}_active = yes }}'))
    emit('common/decisions/' + stem + '.txt', block(stem + '_programmes', ''.join(decisions)))


def apply_service(tag, domain, policy):
    return ''.join('remove_ideas = ' + tag + '_wc_' + domain + '_' + str(i) + '\n' for i in range(3)) + \
        f'add_timed_idea = {{ idea = {tag}_wc_{domain}_{policy} days = 365 }}\n'


def add_focus(target, tag, chapter, ident, title, x, y, prereq, reward, explanation, condition=''):
    loc(ident, title)
    loc(ident + '_desc', chapter.problem + '\\n\\n' + explanation + '\\n\\nOriginal national campaign fiction and provisional gameplay.')
    target.append(block('focus', f'id = {ident}\nicon = GFX_{tag}_wc_{chapter.domain}\nx = {x}\ny = {y}\ncost = 5\ncancel_if_invalid = yes\n' + prereq +
        block('available', (f'ac_wc_{tag.lower()}_active = yes ' + condition).rstrip()) +
        block('completion_reward', reward) + block('ai_will_do', 'factor = 1')))


def decision(ident, title, desc, visible, available, effect, cost=25, cooldown=30, extra=''):
    loc(ident, title)
    loc(ident + '_desc', desc)
    return block(ident, 'icon = ' + ident[:3] + '_wc_civil\n' + block('visible', visible) +
        block('available', available) + f'cost = {cost}\nfire_only_once = no\ndays_re_enable = {cooldown}\n' +
        block('complete_effect', effect) + extra + block('ai_will_do', 'base = 1'))


def outputs():
    OUT.clear(); LOC.clear(); ROWS.clear()
    common()
    for tag, chapters in COUNTRIES.items():
        country(tag, chapters)
    relations()
    for tag in COUNTRIES:
        # Independent migration decision: initial selection is engine-owned;
        # saved generic/regional trees are replaced only while both are idle.
        ident = tag + '_wc_adopt'
        loc(ident, 'Open the National Campaign')
        loc(ident + '_desc', 'Adopt the dedicated national campaign from an idle generic or regional tree. Completed focuses remain recorded. No starting forces, industry, fiscal account or old historical rewards are reseeded.')
        path = 'common/decisions/ac_wc_' + tag.lower() + '.txt'
        current = OUT[path].decode()
        extra = decision(ident, LOC[ident], LOC[ident+'_desc'],
            f'ac_wc_{tag.lower()}_active = yes OR = {{ has_focus_tree = generic_focus has_focus_tree = ac_regional_foundation }}',
            'ac_pol_previous_tree_idle = yes',
            guard('ac_pol_previous_tree_idle = yes', f'load_focus_tree = {{ tree = ac_wc_{tag.lower()}_tree keep_completed = yes }}'), cost=0)
        at = current.rfind('}')
        OUT[path] = (current[:at] + extra + current[at:]).encode()
    loc('ac_wc_programmes', 'National Programmes')
    OUT['localisation/english/ac_world_campaigns_l_english.yml'] = ('\ufeffl_english:\n' + ''.join(
        ' ' + key + ':0 "' + value.replace('"', '\\"') + '"\n' for key, value in sorted(LOC.items()))).encode('utf-8')
    return OUT


def relations():
    """Fixed bilateral requests; no factions, annexations or compulsory replies."""
    loc('ac_wc_partner_tt', 'Both independent governments can answer and are at peace with each other')
    events = []
    for index, (sender, receiver, chapter) in enumerate([('SOA', 'CSO', 'central'), ('SOA', 'FCU', 'fcu'), ('CSO', 'SOA', 'sotoa')], 1):
        request = sender + '_wc_contact_' + receiver.lower()
        pending = flag(request + '_pending', 'A limited contact invitation is awaiting a reply')
        answered = flag(request + '_answered', 'The invited government answered the current invitation')
        accepted = flag(request + '_accepted', 'The invited government accepted limited contact')
        refused = flag(request + '_refused', 'The invited government declined limited contact')
        valid = f'tag = {receiver} original_tag = {receiver} is_subject = no has_capitulated = no any_owned_state = {{ is_controlled_by = PREV }} has_war_with = {sender}'
        valid = valid.replace(f'has_war_with = {sender}', f'NOT = {{ has_war_with = {sender} }}')
        from_valid = f'tag = {sender} original_tag = {sender} is_subject = no has_capitulated = no any_owned_state = {{ is_controlled_by = PREV }} has_country_flag = {pending}'
        reply = block('custom_trigger_tooltip', 'tooltip = ac_wc_partner_tt\n' + valid + '\n' + block('FROM', from_valid))
        event_id = 'ac_wc_relations.' + str(index)
        options = ''
        for choice, title in [('accept', 'Accept a limited reciprocal mission'), ('refuse', 'Decline without further obligations')]:
            loc(event_id + '.' + choice, title)
            mark = accepted if choice == 'accept' else refused
            body = f'clr_country_flag = {pending}\nset_country_flag = {answered}\nset_country_flag = {mark}\n'
            if choice == 'accept':
                body += f'add_opinion_modifier = {{ target = {receiver} modifier = ac_wc_contact_opinion }}\n'
            response = block('FROM', body)
            if choice == 'accept':
                response += f'add_opinion_modifier = {{ target = {sender} modifier = ac_wc_contact_opinion }}\n'
            options += block('option', f'name = {event_id}.{choice}\n' + block('trigger', reply) +
                block('ai_chance', 'factor = ' + ('60' if choice == 'accept' else '40')) + guard(reply, response))
        loc(event_id + '.close', 'Close the expired or ineligible invitation')
        options += block('option', f'name = {event_id}.close\n' + block('trigger', block('NOT', reply)))
        loc(event_id + '.t', 'An Invitation From ' + ('Sotoa' if sender == 'SOA' else 'Central Sotoa'))
        loc(event_id + '.d', 'The other government proposes a limited civilian and technical contact mission. Acceptance improves mutual opinion for one year. It creates no alliance, access right, financial obligation or claim over territory. A refusal leaves both governments free to pursue domestic training. This exchange is original campaign fiction; it is not an official historical agreement.')
        events.append(block('country_event', f'id = {event_id}\ntitle = {event_id}.t\ndesc = {event_id}.d\nis_triggered_only = yes\npicture = GFX_{sender}_wc_scene_diplomacy\n' + options))
        ready = 'OR = { ' + ' '.join(f'has_completed_focus = {sender}_wc_e1_{chapter}_p{i}_1' for i in range(3)) + ' }'
        condition = f'is_subject = no NOT = {{ has_country_flag = {pending} }}\n' + block(receiver, valid + ' exists = yes')
        request_body = guard(condition,
            f'clr_country_flag = {answered}\nclr_country_flag = {accepted}\nclr_country_flag = {refused}\nset_country_flag = {{ flag = {pending} days = 45 }}\n' + block(receiver, f'country_event = {{ id = {event_id} days = 1 }}'))
        row = decision(request, 'Invite ' + ('Central Sotoa' if receiver == 'CSO' else 'Central Usea' if receiver == 'FCU' else 'Sotoa'),
            'Pay 25 political power to offer a limited contact mission. Both governments must be independent, control territory, and remain at peace with each other. The invitation expires in 45 days. Refusal or silence grants no benefit; the domestic programme remains available.',
            f'ac_wc_{sender.lower()}_active = yes {ready}', condition, request_body, cooldown=365)
        path = 'common/decisions/ac_wc_' + sender.lower() + '.txt'
        current = OUT[path].decode(); at = current.rfind('}')
        OUT[path] = (current[:at] + row + current[at:]).encode()
    emit('events/ac_wc_relations.txt', 'add_namespace = ac_wc_relations\n' + ''.join(events))
    loc('ac_wc_contact_opinion', 'Reciprocal technical contact')
    emit('common/opinion_modifiers/ac_wc_relations.txt', block('opinion_modifiers', block('ac_wc_contact_opinion', 'value = 10\ndays = 365')))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = outputs()
    failed = []
    for relative, data in result.items():
        path = MOD / relative
        if args.check:
            if not path.exists() or path.read_bytes().replace(b'\r\n', b'\n') != data:
                failed.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    manifest = json.dumps(dict(schema=1, source_layer='original fiction / provisional gameplay',
        reference=SOURCE, chapters=ROWS, native_acceptance=False), indent=2) + '\n'
    path = HERE / 'sotoa_content.json'
    if args.check:
        if path.read_text() != manifest:
            failed.append('sotoa_content.json')
    else:
        path.write_text(manifest, encoding='utf-8', newline='\n')
    if failed:
        raise SystemExit('Generated source differs: ' + ', '.join(failed))
    print(f'Sotoan opening: {sum(len(r["focuses"]) for r in ROWS)} focuses, {len(ROWS)+3} choice events, {len(ROWS)*3+5} decisions; native pending.')


if __name__ == '__main__':
    main()
