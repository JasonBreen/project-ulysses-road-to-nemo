"""Focus visibility and size: the definition of done for the 150-focus programme.

Static and offline. A focus is *visible* when its node resolves on screen
(x, y >= 0), its caption does not collide with a neighbour on the same row, it
has a localised title and description, its icon sprite is defined in the mod
with an existing texture, and no condition hides a country's own branch.

Size is a ratchet. Every country in scope plays, from 1 January 1991, the tree
its `country` weights select, and every tree it can be on is counted with its
imports. ``docs/evidence/focus-visibility/baseline.json`` records each tree's
floor; a floor never falls, waves raise it, and the programme target is 150.

    python -B tools/Test-FocusVisibility.py            # check
    python -B tools/Test-FocusVisibility.py --record   # raise floors after a wave (never lowers one)
    python -B tools/Test-FocusVisibility.py --report   # progress toward 150
"""
import argparse
import datetime
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
import focus_layout  # noqa: E402
from script import parse, get  # noqa: E402

BASELINE = ROOT / 'docs/evidence/focus-visibility/baseline.json'
TARGET = 150
START = datetime.date(1991, 1, 1)
# Countries that own no land on 1 January 1991 but can be released, and have or
# will have a tree of their own. PLH ("Place Holder", state 171) is out of scope
# under AGENTS.md.
RELEASES = ('REC', 'SBK', 'AWW', 'SHI', 'REL', 'SER', 'TER')
EXCLUDED = ('PLH',)
# Trees without a country weight that a scripted owner loads for one country.
LOADED = {'ac_ucw_eru_tree': 'ERU', 'ac_ucw_fcu_tree': 'FCU'}
# The generic tree keeps the base game's own localisation keys.
VANILLA_TEXT_TREES = ('generic_focus',)
# Inherited Belkan chain gates: allow_branch on focus completion, reviewed and kept.
ALLOWED_GATES = {'BLK_party_disagreements', 'BLK_nationalism_unleashed', 'BLK_taking_off_the_kid_gloves'}


def opening_gate(gate):
    """allow_branch that hides a branch only until its era opens: tag keys plus one OR of
    an opening date or start flag and the branch's own progress (has_completed_focus)."""
    rest = [(key, value) for key, _, value in gate if key not in ('tag', 'original_tag')]
    if len(rest) != 1 or rest[0][0] != 'OR' or not isinstance(rest[0][1], list):
        return False
    kinds = set()
    for key, op, value in rest[0][1]:
        if key == 'date' and op == '>':
            kinds.add('opening')
        elif key == 'has_country_flag' and isinstance(value, str) and re.match(r'ac_\w+_started$', value):
            kinds.add('opening')
        elif key == 'has_completed_focus':
            kinds.add('progress')
        else:
            return False
    return kinds == {'opening', 'progress'}


def trees_and_focuses(mod=MOD):
    trees, focuses = {}, {}
    for path in sorted((mod / 'common/national_focus').glob('*.txt'), key=lambda p: p.as_posix()):
        for kind, _, node in parse(path.read_text(encoding='utf-8-sig')):
            if kind == 'shared_focus' and isinstance(node, list):
                focuses[get(node, 'id')] = node
            elif kind == 'focus_tree':
                trees[get(node, 'id')] = node
                for key, _, child in node:
                    if key == 'focus' and isinstance(child, list):
                        focuses[get(child, 'id')] = child
    return trees, focuses


def regional_tags(mod=MOD):
    text = (mod / 'common/scripted_triggers/ac_politics.txt').read_text(encoding='utf-8-sig')
    body = text[text.index('ac_pol_uses_regional_tree = {'):]
    return set(re.findall(r'original_tag = ([A-Z0-9]{3})', body[:body.index('\n}\n')]))


def holds(nodes, tag, regional):
    """Evaluate a country-weight condition for a tag on 1 January 1991."""
    for key, op, value in nodes:
        if key in ('tag', 'original_tag'):
            answer = value == tag
        elif key == 'ac_pol_uses_regional_tree':
            answer = (tag in regional) == (value == 'yes')
        elif key == 'has_global_flag':
            answer = False
        elif key == 'date':
            day = datetime.date(*map(int, value.split('.')))
            answer = START < day if op == '<' else START > day
        elif key == 'NOT':
            answer = not any(holds([row], tag, regional) for row in value)
        elif key == 'OR':
            answer = any(holds([row], tag, regional) for row in value)
        elif key == 'AND':
            answer = holds(value, tag, regional)
        elif key == 'add':
            continue
        else:
            raise ValueError('Unmodelled focus-tree weight condition: ' + key)
        if not answer:
            return False
    return True


def weight(tree, tag, regional):
    country = get(tree, 'country') or []
    total = float(get(country, 'factor', '0'))
    for key, _, value in country:
        if key == 'modifier' and holds(value, tag, regional):
            total += float(get(value, 'add', '0'))
    return total


def scope(mod=MOD):
    owners = set()
    for path in (mod / 'history/states').glob('*.txt'):
        match = re.search(r'\bowner\s*=\s*([A-Z0-9]{3})', path.read_text(encoding='utf-8-sig', errors='replace'))
        if match:
            owners.add(match[1])
    return sorted((owners | set(RELEASES)) - set(EXCLUDED))


def script_loaded(mod=MOD):
    """Trees a decision loads for exactly one country (Usea Depth adopt decisions, for example)."""
    loaded = dict(LOADED)
    for path in sorted((mod / 'common/decisions').glob('*.txt')):
        for _, _, category in parse(path.read_text(encoding='utf-8-sig')):
            for _, _, decision in category if isinstance(category, list) else ():
                if not isinstance(decision, list):
                    continue
                text = repr(decision)
                trees = set(re.findall(r"\['load_focus_tree', '=', \[\['tree', '=', '(\w+)'\]", text))
                trees |= set(re.findall(r"\['load_focus_tree', '=', '(\w+)'\]", text))
                tags = set(re.findall(r"\['original_tag', '=', '([A-Z0-9]{3})'\]", text))
                if len(tags) == 1:
                    for tree in trees:
                        loaded.setdefault(tree, next(iter(tags)))
    return loaded


def census(mod=MOD):
    """Per tag: the start trees (all tied at the top weight) and every tree it can be on."""
    trees, _ = trees_and_focuses(mod)
    positions = focus_layout.resolved_tree_positions(mod)
    regional = regional_tags(mod)
    loaded = script_loaded(mod)
    result = {}
    for tag in scope(mod):
        weights = {ident: weight(tree, tag, regional) for ident, tree in trees.items()}
        best = max(weights.values())
        start = sorted(ident for ident, w in weights.items() if w == best)
        reachable = sorted({ident for ident, w in weights.items() if w > 0} | set(start) |
                           {ident for ident, owner in loaded.items() if owner == tag and ident in trees})
        result[tag] = {'start': start, 'trees': {ident: len(positions[ident]) for ident in reachable}}
    return result


def tree_floors(data):
    floors = {}
    for row in data.values():
        for ident, count in row['trees'].items():
            floors[ident] = count
    return dict(sorted(floors.items()))


def localisation_keys(mod=MOD):
    keys = set()
    for path in (mod / 'localisation').rglob('*.yml'):
        for line in path.read_text(encoding='utf-8-sig', errors='replace').splitlines():
            match = re.match(r'\s*([A-Za-z0-9_.\-]+):\d*\s*"', line)
            if match:
                keys.add(match[1])
    return keys


def mod_sprites(mod=MOD):
    sprites = {}
    for path in (mod / 'interface').glob('*.gfx'):
        text = path.read_text(encoding='utf-8-sig', errors='replace')
        for match in re.finditer(r'name\s*=\s*"?(GFX_[^"\s]+)"?\s*texturefile\s*=\s*"([^"]+)"', text):
            sprites[match[1]] = match[2]
    return sprites


class FocusVisibility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trees, cls.focuses = trees_and_focuses()
        cls.positions = focus_layout.resolved_tree_positions()
        cls.census = census()

    def test_every_node_resolves_on_screen(self):
        off = {tree: sorted(f for f, (x, y) in nodes.items() if x < 0 or y < 0) for tree, nodes in self.positions.items()}
        self.assertEqual({}, {tree: ids for tree, ids in off.items() if ids})

    def test_no_two_captions_share_a_row_slot(self):
        clashes = []
        for tree, nodes in self.positions.items():
            rows = {}
            for ident, (x, y) in nodes.items():
                rows.setdefault(y, []).append((x, ident))
            for row in rows.values():
                row.sort()
                clashes += [(tree, a, b) for (xa, a), (xb, b) in zip(row, row[1:]) if xb - xa < 2]
        self.assertEqual([], clashes)

    def test_every_focus_has_text_and_a_mod_icon(self):
        keys, sprites = localisation_keys(), mod_sprites()
        vanilla_text = {f for tree in VANILLA_TEXT_TREES for f in self.positions[tree]}
        missing_text, missing_icon = [], []
        for tree, nodes in sorted(self.positions.items()):
            for ident in sorted(nodes):
                if ident not in vanilla_text and (ident not in keys or ident + '_desc' not in keys):
                    missing_text.append((tree, ident))
                icon = (get(self.focuses[ident], 'icon') or '').strip('"')
                texture = sprites.get(icon)
                if not texture or not (MOD / texture).is_file():
                    missing_icon.append((tree, ident, icon))
        self.assertEqual([], missing_text)
        self.assertEqual([], missing_icon)

    def test_no_condition_hides_a_country_own_branch(self):
        hidden = []
        for ident, node in self.focuses.items():
            gate = get(node, 'allow_branch')
            if gate is None:
                continue
            tag_only = all(key in ('tag', 'original_tag') for key, _, _ in gate)
            if not tag_only and ident not in ALLOWED_GATES and not opening_gate(gate):
                hidden.append(ident)
        self.assertEqual([], hidden)
        # Opening gates hide a branch only until its era opens; the owners must redraw the
        # screen when it does (main f70dc7b5: weekly tick and ac_pwi_start refresh the layout).
        effects = ''.join(p.read_text(encoding='utf-8-sig') for p in (MOD / 'common/scripted_effects').glob('*.txt'))
        if any(opening_gate(get(n, 'allow_branch')) for n in self.focuses.values() if get(n, 'allow_branch') is not None):
            self.assertIn('mark_focus_tree_layout_dirty', effects)

    def test_initial_show_positions_name_a_focus_in_their_tree(self):
        for ident, tree in self.trees.items():
            show = get(tree, 'initial_show_position')
            if show and get(show, 'focus'):
                self.assertIn(get(show, 'focus'), self.positions[ident], ident)

    def test_every_country_in_scope_has_a_tree_and_no_floor_falls(self):
        baseline = json.loads(BASELINE.read_text(encoding='utf-8'))
        self.assertEqual(TARGET, baseline['target'])
        self.assertEqual(sorted(baseline['countries']), sorted(self.census))
        for tag, row in self.census.items():
            with self.subTest(tag=tag):
                self.assertTrue(row['start'], 'no start tree')
                for ident, count in row['trees'].items():
                    self.assertGreaterEqual(count, baseline['tree_floors'].get(ident, 0), ident + ' fell below its recorded floor')


def report(data):
    floors = tree_floors(data)
    below = {ident: count for ident, count in floors.items() if count < TARGET}
    print('Countries in scope: %d; trees they can be on: %d; at %d+: %d; below: %d; focuses still needed: %d' % (
        len(data), len(floors), TARGET, len(floors) - len(below), len(below), sum(TARGET - c for c in below.values())))
    generic = sorted(tag for tag, row in data.items() if row['start'] in (['generic_focus'], ['ac_regional_foundation']))
    print('Countries still starting on the generic or regional tree (%d): %s' % (len(generic), ' '.join(generic)))


def record(data):
    floors = tree_floors(data)
    previous = json.loads(BASELINE.read_text(encoding='utf-8')) if BASELINE.exists() else {'tree_floors': {}}
    lowered = {ident: (old, floors.get(ident)) for ident, old in previous['tree_floors'].items() if floors.get(ident, 0) < old}
    if lowered:
        raise SystemExit('Refusing to lower a floor: ' + json.dumps(lowered))
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    BASELINE.write_text(json.dumps(dict(target=TARGET, excluded=list(EXCLUDED), releases=list(RELEASES),
                                        countries={tag: row['start'] for tag, row in data.items()},
                                        tree_floors=floors), indent=1) + '\n', encoding='utf-8', newline='\n')
    print('Recorded %d tree floors for %d countries' % (len(floors), len(data)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--record', action='store_true')
    parser.add_argument('--report', action='store_true')
    args, rest = parser.parse_known_args()
    if args.record or args.report:
        data = census()
        if args.record:
            record(data)
        report(data)
    else:
        unittest.main(argv=[sys.argv[0]] + rest)
