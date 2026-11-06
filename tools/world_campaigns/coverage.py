"""Country/era delivery accounting. Reservations are never delivered content."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
from script import parse, get, walk

PRINCIPAL = set('SOA BLK UST OSE YUK ERU FCU EMM EVA AUR LEA'.split())
REGIONAL = set('SAP GEB FAT SNS AMB NPT NEC WEL ARK PBL NRL'.split())
EMERGENT = set('AWW REC SBK REL SER SHI TER'.split())
ERAS = [('e1', 1991, 2005), ('e2', 2006, 2020), ('e3', 2021, 2040)]
BASE = '38c978d0a848df7b173a6f71b5f231ef6e83e447'
RESERVATIONS = {
    'eru': (82, '85b4a8d5bb24260244120de019891b29b38b8596'),
    'fcu': (81, '55d379185860c0c607fdf796bd50a5a9529a408c'),
    'npt': (79, 'a9252c0a0b40761c960faeb7de9ba9599cf0b1e1'),
    'partners': (78, '6045cc9e3b057ee626e01ee21c01b43c01f45bf8'),
    'minors_a': (77, '2e5629eb8fda2524a62b8f740e2d253704d7fe9f'),
    'minors_b': (80, '6d9963e8aaa79ae59e33b451f3ca57e7aac7d085'),
}


def git_text(ref, path):
    return subprocess.check_output(['git', 'show', ref + ':' + path], cwd=ROOT).decode('utf-8-sig')


def reservation_ids(head, counts):
    """Capture once from the exact PR receipt; normal checks need no Git objects."""
    ids = {tag: set() for tag in counts}
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', head,
                                    'mod/2985041246/common/national_focus'], cwd=ROOT).decode().splitlines()
    for path in paths:
        if 'ac_ud_' not in path:
            continue
        for kind, node in walk(parse(git_text(head, path))):
            if kind in ('focus', 'shared_focus'):
                ident = get(node, 'id', '')
                if ident[:3] in ids and ident.startswith(ident[:3] + '_ud_'):
                    ids[ident[:3]].add(ident)
    if {tag: len(values) for tag, values in ids.items()} != counts:
        raise ValueError('Reserved PR IDs differ from the budget at ' + head)
    return {tag: sorted(values) for tag, values in ids.items()}


def pending_reservation_ids(reservations, tag, delivered_ids):
    promised = set()
    for row in reservations:
        ids = row['focus_ids'][tag]
        if len(ids) != row['focuses'][tag] or len(set(ids)) != len(ids):
            raise ValueError('Reserved ID receipt differs from its budget')
        if promised.intersection(ids):
            raise ValueError('Duplicate reservation ownership for ' + tag)
        promised.update(ids)
    return promised - set(delivered_ids)


def inventory(sources):
    """Resolve actual import closure; exclude orphaned definitions from credit."""
    definitions, trees, children = {}, [], defaultdict(set)
    for path, text in sources:
        for kind, _, node in parse(text):
            if kind not in ('focus_tree', 'shared_focus') or not isinstance(node, list):
                continue
            if kind == 'shared_focus':
                ident = get(node, 'id')
                if ident in definitions:
                    raise ValueError('Duplicate focus: ' + ident)
                definitions[ident] = (node, path)
            else:
                trees.append((get(node, 'id'), node, path))
                for key, _, child in node:
                    if key == 'focus' and isinstance(child, list):
                        ident = get(child, 'id')
                        if ident in definitions:
                            raise ValueError('Duplicate focus: ' + ident)
                        definitions[ident] = (child, path)
    for ident, (node, _) in definitions.items():
        for key, _, body in node:
            if key == 'prerequisite':
                for field, _, ref in body:
                    if field == 'focus':
                        children[ref].add(ident)
    bound = defaultdict(set)
    for tree_id, tree, path in trees:
        pending = [get(n, 'id') if isinstance(n, list) else n for k, _, n in tree if k in ('focus', 'shared_focus')]
        seen = set()
        while pending:
            ident = pending.pop()
            if ident in seen:
                continue
            seen.add(ident)
            if ident not in definitions:
                raise ValueError('Unresolved import: ' + tree_id + ':' + ident)
            bound[ident].add(tree_id)
            pending.extend(children[ident])
    years = {}
    def earliest(ident, stack=()):
        if ident in years:
            return years[ident]
        if ident in stack:
            raise ValueError('Prerequisite cycle: ' + ident)
        node = definitions[ident][0]
        dates = [int(v[:4]) for k, n in walk(node) for f, op, v in n
                 if k == 'available' and f == 'date' and op in ('>', '>=') and isinstance(v, str) and re.match(r'\d{4}\.', v)]
        parents = [v for k, _, n in node if k == 'prerequisite' for f, _, v in n if f == 'focus' and v in definitions]
        years[ident] = max([1991, *dates, *(earliest(p, stack + (ident,)) for p in parents)])
        return years[ident]
    rows = []
    for ident, (node, path) in sorted(definitions.items()):
        if not re.match(r'^[A-Z]{3}_', ident) or ident not in bound:
            continue
        year = earliest(ident)
        era = next((key for key, start, end in ERAS if start <= year <= end), None)
        rows.append(dict(id=ident, tag=ident[:3], era=era, earliest_literal_or_prerequisite_year=year,
                         source=path, imported_by=sorted(bound[ident]),
                         source_layer='existing mod provenance / provisional gameplay',
                         date_inference='Accounting estimate, not a claim of native reachability or canon date'))
    return rows


def capture():
    target = HERE / 'baseline.json'
    if target.exists():
        raise ValueError('Refusing to overwrite the frozen baseline')
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE,
                                    'mod/2985041246/common/national_focus'], cwd=ROOT).decode().splitlines()
    sources = [(p, git_text(BASE, p)) for p in paths]
    baseline = dict(schema=1, commit=BASE, focuses=inventory(sources), reservations=[])
    for package, (pr, head) in RESERVATIONS.items():
        path = f'tools/usea_depth/{package}/budget.json'
        raw = git_text(head, path)
        budget = json.loads(raw)
        baseline['reservations'].append(dict(package=package, pull_request=pr, head=head,
            reference=f'https://github.com/JasonBreen/project-ulysses-road-to-nemo/pull/{pr}',
            path=path, sha256=hashlib.sha256(raw.encode()).hexdigest(), era='e1',
            focuses=budget['focuses'], focus_ids=reservation_ids(head,budget['focuses']),
            status='reserved external PR at capture; source integration is recalculated from actual IDs'))
    target.write_text(json.dumps(baseline, indent=2) + '\n', encoding='utf-8', newline='\n')


def report():
    baseline = json.loads((HERE / 'baseline.json').read_text())
    registry = json.loads((ROOT / 'tools/world_foundation/country_registry.json').read_text())
    sources = [(p.relative_to(ROOT).as_posix(), p.read_text(encoding='utf-8-sig'))
               for p in sorted((MOD / 'common/national_focus').glob('*.txt'))]
    actual = inventory(sources)
    by_era = defaultdict(list)
    source_ids = defaultdict(set)
    for row in actual:
        by_era[row['tag'], row['era']].append(row)
        source_ids[row['tag']].add(row['id'])
    rows = []
    for country in sorted(registry['countries'], key=lambda c: c['tag']):
        tag = country['tag']
        if tag == 'PLH':
            continue
        group = 'principal' if tag in PRINCIPAL else 'regional' if tag in REGIONAL else 'emergent' if tag in EMERGENT else 'other_active'
        target = dict(principal=240, regional=120, emergent=80, other_active=80)[group]
        allocations = []
        for era, start, end in ERAS:
            existing = [r for r in baseline['focuses'] if r['tag'] == tag and r['era'] == era]
            reservations = [r for r in baseline['reservations'] if r['era'] == era and tag in r['focuses']]
            current = by_era[tag, era]
            actual_ids = {r['id'] for r in current}
            reserved_at_approval = sum(r['focuses'][tag] for r in reservations)
            # A delivered ID is not pending even if its actual date gates put
            # it in a different era than the original reservation estimate.
            reserved = len(pending_reservation_ids(reservations, tag, source_ids[tag]))
            allocations.append(dict(era=era, years=[start, end], target=target,
                baseline_ids=[r['id'] for r in existing], baseline_owners=sorted({r['source'] for r in existing}),
                reserved_at_approval=reserved_at_approval, reserved_additions=reserved,
                reserved_now_in_source=reserved_at_approval-reserved,
                reservation_references=[r['reference'] for r in reservations],
                delivered_count=len(actual_ids), delivered_ids=sorted(actual_ids),
                remaining_actual=max(0, target-len(actual_ids)),
                unreserved_authoring_gap=max(0, target-len(actual_ids)-reserved),
                status='source-defined; native pending' if len(actual_ids) >= target else 'authoring pending',
                native_acceptance=False))
        rows.append(dict(tag=tag, name=country['name'], classification=country['start_classification'],
            tier=group, existing_history=country['history'], source_layer='mod provenance / approved original gameplay',
            reference='Private user approval, 2026-11-06, National campaigns for everyone, 1991–2040',
            appearance='existing legitimate release/outcome only' if tag in EMERGENT else '1991 active start', eras=allocations))
    if len(rows) != 68 or len({r['tag'] for r in rows}) != 68:
        raise ValueError('Expected exactly 68 legitimate countries')
    return dict(schema=1, approval='Private user approval, 2026-11-06, implement the national campaigns/UI plan',
        baseline_commit=BASE, authored_horizon=[1991, 2040], engine_horizon=2065,
        regional_fallback_credited=False, reservations_are_delivered=False, native_acceptance=False,
        countries=rows, summary=dict(countries=68, allocations=204,
            target=sum(e['target'] for r in rows for e in r['eras']),
            delivered=sum(e['delivered_count'] for r in rows for e in r['eras']),
            remaining_actual=sum(e['remaining_actual'] for r in rows for e in r['eras']),
            unreserved_authoring_gap=sum(e['unreserved_authoring_gap'] for r in rows for e in r['eras'])))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--capture', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.capture:
        capture()
    data = report()
    output = json.dumps(data, indent=2) + '\n'
    path = HERE / 'manifest.json'
    if args.check:
        if path.read_text() != output:
            raise SystemExit('World campaign delivery manifest is stale')
    else:
        path.write_text(output, encoding='utf-8', newline='\n')
    print(json.dumps(data['summary']))
    print('Reservations are not deliveries; source definitions are not native acceptance.')


if __name__ == '__main__':
    main()
