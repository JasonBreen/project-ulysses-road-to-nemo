"""Mod-wide wiring audit: everything read is written, everything fired exists.

    python -B tools/wiring/audit.py                     # summary by check
    python -B tools/wiring/audit.py --report            # every active finding
    python -B tools/wiring/audit.py --json out.json     # machine-readable findings
    python -B tools/wiring/audit.py --reference-game-root <read-only HOI4 install>

Severity:
  defect   something is read, fired or called but never written or defined, or
           guarded code does nothing; fix it or allowlist it with a reason
  warning  probably unintended but harmless to the engine (missing text, an
           unimported shared focus, a scripted call missing a parameter)
  info     written but never read, defined but never used; reported, never gated

Names outside the mod's own prefixes (ac_ and its country tags) are vanilla's:
without a reference root they are counted as unverified externals, not findings.
Exceptions live in tools/wiring/allowlist.json, each with a class and a reason.
This is a static source audit; it does not prove that anything fires in game.
"""
import argparse
from collections import Counter, defaultdict
import fnmatch
import json
import os
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from index import Index, is_pattern, name_regex, names_match, shape  # noqa: E402

DEFAULT_MOD = ROOT / 'mod/2985041246'
ALLOWLIST = HERE / 'allowlist.json'
SEVERITY = {
    'parse-unbalanced': 'defect',
    'flag-read-never-set': 'defect',
    'flag-set-never-read': 'info',
    'event-undefined': 'defect',
    'event-duplicate': 'defect',
    'event-no-caller': 'defect',
    'scripted-undefined': 'defect',
    'scripted-param-missing': 'warning',
    'scripted-unused': 'info',
    'idea-undefined': 'defect',
    'idea-unreferenced': 'info',
    'character-undefined': 'defect',
    'decision-undefined': 'defect',
    'category-undefined': 'defect',
    'tree-unassignable': 'defect',
    'tree-load-undefined': 'defect',
    'shared-focus-undefined': 'defect',
    'shared-focus-unimported': 'warning',
    'variable-read-never-set': 'defect',
    'state-undefined': 'defect',
    'province-undefined': 'defect',
    'empty-guarded-block': 'defect',
    'empty-else': 'info',
    'loc-missing': 'warning',
}
GATED = ('defect', 'warning')
EFFECT_FILES = ('events/', 'common/national_focus/', 'common/decisions/', 'common/scripted_effects/',
                'common/scripted_triggers/', 'common/on_actions/', 'history/countries/', 'common/scripted_guis/',
                'common/ideas/', 'common/characters/', 'common/bop/', 'common/special_projects/')


def finding(check, name, ref=None, detail=''):
    return {'check': check, 'severity': SEVERITY[check], 'name': str(name), 'file': ref.file if ref else '',
            'line': ref.line if ref else 0, 'detail': detail}


class Matcher:
    """Fast membership for literal names plus pattern names on either side."""
    def __init__(self, names):
        self.literal = set()
        self.patterns = []
        for name in names:
            if is_pattern(name):
                self.patterns.append(name)
            else:
                self.literal.add(name)
        self.regexes = [(p, name_regex(p)) for p in self.patterns]

    def __contains__(self, name):
        if name in self.literal:
            return True
        if is_pattern(name):
            regex = name_regex(name)
            if any(regex.match(lit) for lit in self.literal):
                return True
            return any(names_match(name, p) for p in self.patterns)
        return any(regex.match(name) for _, regex in self.regexes)


def audit(index):
    out = []
    owned = index.owned
    externals = Counter()

    for problem in index.problems:
        rel, _, text = problem.partition(': ')
        out.append(finding('parse-unbalanced', rel, None, text) | {'file': rel})

    # Flags
    for kind in ('global', 'country', 'state', 'character'):
        sets = Matcher([n for (k, n) in index.flag_set if k == kind])
        reads = Matcher([n for (k, n) in index.flag_read if k == kind])
        for (k, name), refs in sorted(index.flag_read.items()):
            if k == kind and name not in sets:
                out.append(finding('flag-read-never-set', '%s:%s' % (kind, name), refs[0], '%d reads' % len(refs)))
        for (k, name), refs in sorted(index.flag_set.items()):
            if k == kind and name not in reads and not any(r.extra.get('reference') for r in refs):
                out.append(finding('flag-set-never-read', '%s:%s' % (kind, name), refs[0]))

    # Events
    for ident, refs in sorted(index.event_dupes.items()):
        out.append(finding('event-duplicate', ident, refs[0], 'also %s:%d' % (index.events[ident].file, index.events[ident].line)))
    for ident, refs in sorted(index.event_calls.items()):
        if ident in index.events or all(r.extra.get('reference') for r in refs):
            continue
        namespace = ident.split('.')[0]
        if namespace in index.namespaces or index.reference_loaded:
            out.append(finding('event-undefined', ident, refs[0], '%d calls' % len(refs)))
        else:
            externals['event'] += 1
    for ident, ref in sorted(index.events.items()):
        if ref.extra.get('reference') or not ref.extra['triggered']:
            continue
        callers = [r for r in index.event_calls.get(ident, ()) if not (r.file == ref.file and r.line == ref.line)]
        if not callers:
            out.append(finding('event-no-caller', ident, ref, 'is_triggered_only with no caller'))

    # Scripted effects and triggers
    defined = dict(index.scripted['trigger'])
    defined.update(index.scripted['effect'])
    for kind, table in index.scripted.items():
        for name, ref in sorted(table.items()):
            if ref.extra.get('reference'):
                continue
            uses = [u for u in index.key_uses.get(name, ()) if not (u.file == ref.file and u.line == ref.line)]
            if not uses:
                out.append(finding('scripted-unused', name, ref, 'scripted %s' % kind))
    other_names = set(index.ideas) | set(index.decisions) | set(index.categories) | set(index.characters)
    seen_undefined = set()
    for key, ref, passed in index.scripted_calls:
        if key in defined:
            params = defined[key].extra['params']
            missing = sorted(params - passed)
            if missing and passed is not None:
                out.append(finding('scripted-param-missing', '%s(%s)' % (key, ','.join(missing)), ref))
        elif (not passed and owned(key) and key not in other_names and ref.file.startswith(EFFECT_FILES)
              and key not in seen_undefined and not is_pattern(key)):
            seen_undefined.add(key)
            out.append(finding('scripted-undefined', key, ref))

    # Ideas, characters, decisions, categories
    ideas = set(index.ideas) | set(index.idea_tokens)
    for name, refs in sorted(index.idea_uses.items()):
        if name in ideas or is_pattern(name) or name.startswith(('ROOT', 'THIS', 'PREV', 'FROM')):
            continue
        if owned(name) or index.reference_loaded:
            out.append(finding('idea-undefined', name, refs[0], '%d uses' % len(refs)))
        else:
            externals['idea'] += 1
    for name, ref in sorted(index.ideas.items()):
        if not ref.extra.get('reference') and not ref.extra['law'] and name not in index.idea_uses:
            out.append(finding('idea-unreferenced', name, ref, ref.extra['category']))
    for name, refs in sorted(index.character_uses.items()):
        if name in index.characters or is_pattern(name):
            continue
        if owned(name) or index.reference_loaded:
            out.append(finding('character-undefined', name, refs[0]))
        else:
            externals['character'] += 1
    for name, refs in sorted(index.decision_uses.items()):
        if name in index.decisions or is_pattern(name):
            continue
        if owned(name) or index.reference_loaded:
            out.append(finding('decision-undefined', name, refs[0]))
        else:
            externals['decision'] += 1
    for name, refs in sorted(index.category_uses.items()):
        if name in index.categories or is_pattern(name):
            continue
        if owned(name) or index.reference_loaded:
            out.append(finding('category-undefined', name, refs[0]))
        else:
            externals['category'] += 1

    # Focus trees
    for ident, ref in sorted(index.trees.items()):
        if not ref.extra['assignable'] and ident not in index.tree_loads:
            out.append(finding('tree-unassignable', ident, ref, 'no positive country weight and never loaded'))
    for ident, refs in sorted(index.tree_loads.items()):
        if ident not in index.trees and not is_pattern(ident):
            out.append(finding('tree-load-undefined', ident, refs[0]))
    included = set()
    for ident, ref in index.trees.items():
        for imp in ref.extra['imports']:
            if imp.name not in index.shared_focuses:
                out.append(finding('shared-focus-undefined', imp.name, imp))
            included.add(imp.name)
    changed = True
    while changed:
        changed = False
        for ident, ref in index.shared_focuses.items():
            if ident not in included and ref.extra['prerequisites'] & included:
                included.add(ident)
                changed = True
    for ident, ref in sorted(index.shared_focuses.items()):
        if ident not in included:
            out.append(finding('shared-focus-unimported', ident, ref))

    # Variables (the mod's own names only; engine values are read like variables)
    sets = Matcher(index.var_set)
    for name, refs in sorted(index.var_read.items()):
        if name and owned(name) and name not in sets:
            out.append(finding('variable-read-never-set', name, refs[0], '%d reads' % len(refs)))

    # Map ids
    if index.states:
        for state, refs in sorted(index.state_uses.items()):
            if state not in index.states:
                out.append(finding('state-undefined', state, refs[0], '%d uses' % len(refs)))
    if index.provinces:
        for province, refs in sorted(index.province_uses.items()):
            if province not in index.provinces:
                out.append(finding('province-undefined', province, refs[0], '%d uses' % len(refs)))

    # Guarded blocks that do nothing
    for check, refs in (('empty-guarded-block', index.empty_ifs), ('empty-else', index.empty_elses)):
        ordinal = Counter()
        for ref in refs:
            # Stable name (survives line shifts): file, enclosing top-level definition, occurrence.
            label = '%s:%s' % (ref.file, ref.extra['context'])
            ordinal[label] += 1
            out.append(finding(check, '%s#%d' % (label, ordinal[label]), ref))

    # Localisation the script asks for
    for key, refs in sorted(index.loc_wanted.items()):
        if key not in index.loc:
            out.append(finding('loc-missing', key, refs[0]))
    for ident, ref in sorted(index.focuses.items()):
        for key in (ident, ident + '_desc'):
            if key not in index.loc:
                out.append(finding('loc-missing', key, ref, 'focus'))

    return out, externals


def load_allowlist(path=ALLOWLIST):
    if not Path(path).exists():
        return []
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    for entry in data['entries']:
        missing = {'check', 'name', 'class', 'reason', 'layer'} - set(entry)
        if missing:
            raise SystemExit('allowlist entry %r lacks %s' % (entry, ', '.join(sorted(missing))))
        if entry['class'] not in data['classes']:
            raise SystemExit('allowlist entry %r has unknown class' % entry)
    return data['entries']


def apply_allowlist(findings, entries):
    used = Counter()
    active, allowed = [], []
    for f in findings:
        hit = None
        for i, entry in enumerate(entries):
            if entry['check'] == f['check'] and fnmatch.fnmatchcase(f['name'], entry['name']) and \
                    fnmatch.fnmatchcase(f['file'], entry.get('file', '*')):
                hit = i
                break
        if hit is None:
            active.append(f)
        else:
            used[hit] += 1
            allowed.append(dict(f, allow=entries[hit]['class']))
    stale = [entries[i] for i in range(len(entries)) if not used[i]]
    return active, allowed, stale


def key(f):
    return '%s|%s' % (f['check'], f['name'])


def run(mod=DEFAULT_MOD, reference=None, allowlist=ALLOWLIST):
    index = Index(mod, reference)
    findings, externals = audit(index)
    active, allowed, stale = apply_allowlist(findings, load_allowlist(allowlist))
    return index, active, allowed, stale, externals


def summary(active, allowed, externals, index):
    rows = Counter((f['severity'], f['check']) for f in active)
    lines = ['Wiring audit (%s): %d defects, %d warnings, %d info; %d allowlisted; unverified external names: %s' % (
        'with reference game' if index.reference_loaded else 'mod only',
        sum(n for (s, _), n in rows.items() if s == 'defect'), sum(n for (s, _), n in rows.items() if s == 'warning'),
        sum(n for (s, _), n in rows.items() if s == 'info'), len(allowed),
        ', '.join('%s %d' % kv for kv in sorted(externals.items())) or 'none')]
    for (severity, check), n in sorted(rows.items(), key=lambda kv: (('defect', 'warning', 'info').index(kv[0][0]), kv[0][1])):
        lines.append('  %-8s %-26s %6d' % (severity, check, n))
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--mod-root', default=str(DEFAULT_MOD))
    parser.add_argument('--reference-game-root', default=os.environ.get('ULYSSES_GAME_ROOT'))
    parser.add_argument('--report', nargs='?', const='defect,warning', help='list findings of these severities')
    parser.add_argument('--check', help='only this check in --report')
    parser.add_argument('--json')
    args = parser.parse_args()
    index, active, allowed, stale, externals = run(args.mod_root, args.reference_game_root)
    print(summary(active, allowed, externals, index))
    if args.report:
        wanted = set(args.report.split(','))
        for f in sorted(active, key=lambda f: (f['check'], f['name'])):
            if f['severity'] in wanted and (not args.check or f['check'] == args.check):
                print('%-8s %-26s %s  (%s:%d) %s' % (f['severity'], f['check'], f['name'], f['file'], f['line'], f['detail']))
    if stale:
        print('Stale allowlist entries (match nothing): ' + '; '.join('%s %s' % (e['check'], e['name']) for e in stale))
    if args.json:
        Path(args.json).write_text(json.dumps({'active': active, 'allowlisted': allowed, 'externals': externals}, indent=1) + '\n',
                                   encoding='utf-8')


if __name__ == '__main__':
    main()
