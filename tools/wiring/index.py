"""Definition/use index of the mod's script, for the wiring audit.

Reads every script file once with a small brace-aware parser (comments
stripped, line numbers kept) and records where each name is defined and used:
flags, events, scripted effects and triggers, ideas, characters, decisions and
categories, focus trees and shared focuses, variables, states, provinces and
localisation keys. Interpolated names ($param$, [?var], @TAG) are stored as
patterns so they match the names they can expand to.

With a read-only reference game root, the same folders of the installed game
are indexed too, honouring the descriptor's replace_path entries and same-path
overrides, so vanilla names resolve instead of being left unverified.
"""
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
import re

TOKEN = re.compile(r'"(?:\\.|[^"\\\n])*"|#[^\n]*|\n|>=|<=|!=|[{}=<>]|[^\s{}=<>#"]+')
OPS = {'=', '<', '>', '<=', '>=', '!='}
EVENT_TYPES = {'country_event', 'news_event', 'state_event', 'unit_leader_event', 'operative_leader_event'}
FLAG_SET = {'set_country_flag': 'country', 'set_global_flag': 'global', 'set_state_flag': 'state',
            'modify_country_flag': 'country', 'modify_global_flag': 'global', 'modify_state_flag': 'state',
            'set_character_flag': 'character', 'set_unit_leader_flag': 'character', 'set_leader_flag': 'character'}
FLAG_READ = {'has_country_flag': 'country', 'has_global_flag': 'global', 'has_state_flag': 'state',
             'has_character_flag': 'character', 'has_unit_leader_flag': 'character'}
IDEA_USE = {'add_ideas', 'remove_ideas', 'has_idea', 'show_ideas_tooltip', 'add_timed_idea', 'modify_timed_idea',
            'remove_idea', 'add_idea', 'idea'}
CHARACTER_USE = {'recruit_character', 'retire_character', 'has_character', 'promote_character', 'character',
                 'set_nationality_character', 'remove_unit_leader_role', 'add_country_leader_role', 'show_unit_leaders_tooltip'}
DECISION_USE = {'activate_decision', 'activate_targeted_decision', 'activate_mission', 'has_decision', 'has_active_mission',
                'unlock_decision_tooltip', 'remove_decision', 'remove_mission', 'remove_targeted_decision', 'decision'}
CATEGORY_USE = {'unlock_decision_category_tooltip'}
VAR_SET = {'set_variable', 'add_to_variable', 'subtract_from_variable', 'multiply_variable', 'divide_variable',
           'modulo_variable', 'clamp_variable', 'round_variable', 'set_variable_to_random', 'add_to_array',
           'remove_from_array', 'clear_array', 'resize_array', 'add_to_temp_array', 'set_temp_variable',
           'add_to_temp_variable', 'subtract_from_temp_variable', 'multiply_temp_variable', 'divide_temp_variable',
           'clamp_temp_variable', 'round_temp_variable', 'set_temp_variable_to_random', 'find_highest_in_array',
           'find_lowest_in_array'}
STATE_USE = {'owns_state', 'controls_state', 'add_state_core', 'remove_state_core', 'add_state_claim',
             'remove_state_claim', 'transfer_state', 'state', 'has_full_control_of_state', 'is_core_of_state'}
PROVINCE_USE = {'controls_province', 'province'}
COMMON_WORDS = {'set', 'add', 'has', 'may', 'del', 'cal', 'fat', 'rat', 'ark', 'sea', 'air', 'all', 'any', 'one', 'war'}
INTERPOLATION = re.compile(r'\$[^$]*\$|\[[^\]]*\]|@[A-Za-z0-9_.:]+|\?[A-Za-z0-9_.:]+')
SCOPE_PREFIX = re.compile(r'^(?:var:)?(?:(?:global|ROOT|THIS|PREV|FROM|[A-Z]{3}|[A-Z][A-Z0-9]{2}|\d+)\.)+', re.I)


@dataclass
class Node:
    key: str
    op: object
    value: object
    line: int


@dataclass
class Ref:
    name: str
    file: str
    line: int
    extra: dict = field(default_factory=dict)


def parse(text):
    """Return (nodes, problems). Never raises: unbalanced braces are reported."""
    problems = []
    line = 1
    toks = []
    for tok in TOKEN.findall(text):
        if tok == '\n':
            line += 1
        elif not tok.startswith('#'):
            toks.append((tok, line))
    pos = 0
    n = len(toks)

    def block(depth):
        nonlocal pos
        out = []
        while pos < n:
            key, ln = toks[pos]
            pos += 1
            if key == '}':
                if depth:
                    return out
                problems.append('unexpected } at line %d' % ln)
                continue
            if key == '{':
                out.append(Node('', '=', block(depth + 1), ln))
                continue
            if pos < n and toks[pos][0] in OPS:
                op = toks[pos][0]
                pos += 1
                if pos >= n:
                    break
                value, _ = toks[pos]
                pos += 1
                if value == '{':
                    value = block(depth + 1)
                out.append(Node(key, op, value, ln))
            else:
                out.append(Node(key, None, None, ln))
        if depth:
            problems.append('unclosed block (depth %d) at end of file' % depth)
        return out
    return block(0), problems


def unquote(value):
    return value[1:-1] if isinstance(value, str) and len(value) >= 2 and value[0] == '"' == value[-1] else value


def is_pattern(name):
    return bool(INTERPOLATION.search(name))


def name_regex(name):
    parts, last = [], 0
    for m in INTERPOLATION.finditer(name):
        parts.append(re.escape(name[last:m.start()]))
        parts.append('@.+' if m.group(0).startswith('@') else '.+')
        last = m.end()
    parts.append(re.escape(name[last:]))
    return re.compile(''.join(parts) + r'\Z', re.I)


def shape(name):
    return INTERPOLATION.sub(lambda m: '@X' if m.group(0).startswith('@') else 'X', name)


def names_match(a, b):
    if a == b:
        return True
    if not is_pattern(a) and not is_pattern(b):
        return False
    return bool(name_regex(a).match(shape(b)) or name_regex(b).match(shape(a)))


def child(nodes, key):
    for node in nodes:
        if node.key == key:
            return node.value
    return None


def children(nodes, key):
    return [node.value for node in nodes if node.key == key]


def scalars(value):
    """Bare names in a scalar or a list block like { a b c }."""
    if isinstance(value, str):
        return [unquote(value)]
    if isinstance(value, list):
        return [unquote(node.key) for node in value if node.op is None and node.key]
    return []


def plain_var(name):
    name = unquote(name).split('^')[0].split('|')[0].split('@')[0]
    name = SCOPE_PREFIX.sub('', name)
    if name.startswith('var:'):
        name = name[4:]
    return name


class Index:
    def __init__(self, root, reference_root=None):
        self.root = Path(root)
        self.reference_root = Path(reference_root) if reference_root else None
        self.problems = []
        self.flag_set = defaultdict(list)     # (kind, name) -> [Ref]
        self.flag_read = defaultdict(list)
        self.flag_clear = defaultdict(list)
        self.events = {}                      # id -> Ref(extra: triggered, mtth, trigger, file)
        self.event_dupes = defaultdict(list)
        self.namespaces = set()
        self.event_calls = defaultdict(list)
        self.scripted = {'effect': {}, 'trigger': {}}   # name -> Ref(extra: params)
        self.key_uses = defaultdict(list)     # every key occurrence that is not a top-level definition
        self.scripted_calls = []              # (name, Ref, passed params or None)
        self.ideas = {}                       # name -> Ref(extra: category, law)
        self.idea_tokens = {}
        self.idea_uses = defaultdict(list)
        self.characters = {}
        self.character_uses = defaultdict(list)
        self.decisions = {}
        self.decision_uses = defaultdict(list)
        self.categories = {}
        self.category_uses = defaultdict(list)
        self.trees = {}                       # id -> Ref(extra: assignable, imports)
        self.shared_focuses = {}              # id -> Ref(extra: prerequisites)
        self.focuses = {}
        self.tree_loads = defaultdict(list)
        self.var_set = defaultdict(list)
        self.var_read = defaultdict(list)
        self.states = set()
        self.provinces = set()
        self.state_uses = defaultdict(list)
        self.province_uses = defaultdict(list)
        self.empty_ifs = []
        self.empty_elses = []
        self.loc = set()
        self.loc_wanted = defaultdict(list)   # key -> [Ref]
        self.tags = set()
        self.external = {'idea': set(), 'event': set(), 'scripted': set(), 'category': set(), 'character': set()}
        self.reference_loaded = False
        self._load()

    # ---------------------------------------------------------------- loading
    def _files(self, root):
        for folder in ('common', 'events', 'history'):
            base = root / folder
            if base.exists():
                yield from sorted(p for p in base.rglob('*.txt') if p.is_file())

    def _read(self, path):
        return path.read_text(encoding='utf-8-sig', errors='replace')

    def _load(self):
        root = self.root
        for path in sorted((root / 'common/country_tags').glob('*.txt')):
            self.tags |= set(re.findall(r'^\s*([A-Z][A-Z0-9]{2})\s*=', self._read(path), re.M))
        for path in sorted((root / 'history/states').glob('*.txt')):
            match = re.search(r'\bid\s*=\s*(\d+)', re.sub(r'#[^\n]*', '', self._read(path)))
            if match:
                self.states.add(int(match.group(1)))
        definition = root / 'map/definition.csv'
        if definition.exists():
            for row in self._read(definition).splitlines():
                head = row.split(';', 1)[0].strip()
                if head.isdigit():
                    self.provinces.add(int(head))
        for path in sorted((root / 'localisation').rglob('*.yml')):
            for line in self._read(path).splitlines():
                match = re.match(r'\s*([A-Za-z0-9_.\-]+):\d*\s*"', line)
                if match:
                    self.loc.add(match.group(1))
        for path in self._files(root):
            rel = path.relative_to(root).as_posix()
            nodes, problems = parse(self._read(path))
            self.problems += ['%s: %s' % (rel, p) for p in problems]
            self._index_file(rel, nodes)
        if self.reference_root:
            self._load_reference()

    def _load_reference(self):
        """Definitions from a read-only game install, minus replaced paths and same-path overrides."""
        descriptor = self.root / 'descriptor.mod'
        replaced = set(re.findall(r'^\s*replace_path\s*=\s*"([^"]+)"', self._read(descriptor), re.M)) if descriptor.exists() else set()
        for path in self._files(self.reference_root):
            rel = path.relative_to(self.reference_root).as_posix()
            if (self.root / rel).exists() or Path(rel).parent.as_posix() in replaced:
                continue
            nodes, _ = parse(self._read(path))
            self._index_file(rel, nodes, reference=True)
        self.reference_loaded = True

    # ------------------------------------------------------------- indexing
    def _index_file(self, rel, nodes, reference=False):
        parts = rel.split('/')
        folder = parts[1] if parts[0] == 'common' and len(parts) > 2 else parts[0]
        sub = parts[2] if parts[0] == 'common' and len(parts) > 3 else None
        if parts[0] == 'events':
            self._index_events(rel, nodes, reference)
            return
        elif folder in ('scripted_effects', 'scripted_triggers'):
            kind = 'effect' if folder == 'scripted_effects' else 'trigger'
            for node in nodes:
                if isinstance(node.value, list) and not node.key.startswith('@'):
                    params = set(m.split('|')[0] for m in re.findall(r'\$([^$]+)\$', _flat(node.value)))
                    defaults = set(m.split('|')[0] for m in re.findall(r'\$([^$|]+)\|[^$]*\$', _flat(node.value)))
                    self.scripted[kind].setdefault(node.key, Ref(node.key, rel, node.line, {'params': params - defaults, 'reference': reference}))
                    self._walk(rel, node.value, [node.key], reference)
            return
        elif folder == 'ideas':
            for top in nodes:
                if top.key == 'ideas' and isinstance(top.value, list):
                    for cat in top.value:
                        if not isinstance(cat.value, list):
                            continue
                        law = child(cat.value, 'law') == 'yes' or child(cat.value, 'designer') == 'yes'
                        for idea in cat.value:
                            if isinstance(idea.value, list) and idea.key:
                                self.ideas.setdefault(idea.key, Ref(idea.key, rel, idea.line, {'category': cat.key, 'law': law, 'reference': reference}))
        elif folder == 'characters':
            for top in nodes:
                if top.key == 'characters' and isinstance(top.value, list):
                    for char in top.value:
                        if isinstance(char.value, list):
                            self.characters.setdefault(char.key, Ref(char.key, rel, char.line, {'reference': reference}))
                            for role in char.value:
                                if isinstance(role.value, list):
                                    token = child(role.value, 'idea_token')
                                    if token:
                                        self.idea_tokens.setdefault(token, Ref(token, rel, role.line, {'character': char.key}))
        elif folder == 'decisions':
            if sub == 'categories':
                for node in nodes:
                    if isinstance(node.value, list):
                        self.categories.setdefault(node.key, Ref(node.key, rel, node.line, {'reference': reference}))
            elif len(parts) == 3:
                for cat in nodes:
                    if isinstance(cat.value, list):
                        self.category_uses[cat.key].append(Ref(cat.key, rel, cat.line, {'decision_file': True}))
                        for dec in cat.value:
                            if isinstance(dec.value, list):
                                self.decisions.setdefault(dec.key, Ref(dec.key, rel, dec.line, {'category': cat.key, 'reference': reference}))
        elif folder == 'national_focus':
            self._index_focus(rel, nodes, reference)
        self._walk(rel, nodes, [], reference)

    def _index_events(self, rel, nodes, reference):
        for node in nodes:
            if node.key == 'add_namespace' and isinstance(node.value, str):
                if not reference:
                    self.namespaces.add(node.value)
            elif node.key in EVENT_TYPES and isinstance(node.value, list):
                ident = child(node.value, 'id')
                if not ident:
                    continue
                body = node.value
                extra = {'type': node.key, 'triggered': child(body, 'is_triggered_only') == 'yes',
                         'mtth': child(body, 'mean_time_to_happen') is not None, 'trigger': child(body, 'trigger') is not None,
                         'reference': reference}
                ref = Ref(ident, rel, node.line, extra)
                if ident in self.events and not reference:
                    self.event_dupes[ident].append(ref)
                else:
                    self.events.setdefault(ident, ref)
                if not reference:
                    self._index_event_loc(rel, node)
                self._walk(rel, body, [node.key], reference)
            else:
                self._walk(rel, [node], [], reference)

    def _index_event_loc(self, rel, node):
        body = node.value
        if child(body, 'hidden') == 'yes':
            return
        for key in ('title', 'desc'):
            for value in children(body, key):
                if isinstance(value, str):
                    self._want_loc(value, rel, node.line)
                elif isinstance(value, list):
                    text = child(value, 'text')
                    if isinstance(text, str):
                        self._want_loc(text, rel, node.line)
        for option in children(body, 'option'):
            if isinstance(option, list):
                name = child(option, 'name')
                if isinstance(name, str):
                    self._want_loc(name, rel, node.line)

    def _want_loc(self, key, rel, line):
        if key.startswith('"') or '[' in key or '$' in key:
            return
        self.loc_wanted[key].append(Ref(key, rel, line))

    def _index_focus(self, rel, nodes, reference):
        for top in nodes:
            if not isinstance(top.value, list):
                continue
            if top.key == 'focus_tree':
                ident = child(top.value, 'id')
                country = child(top.value, 'country')
                assignable = child(top.value, 'default') == 'yes'
                if isinstance(country, list):
                    factor = child(country, 'factor')
                    try:
                        if factor is not None and float(factor) > 0:
                            assignable = True
                    except ValueError:
                        assignable = True
                    for modifier in children(country, 'modifier'):
                        if isinstance(modifier, list):
                            add = child(modifier, 'add')
                            try:
                                if add is not None and float(add) > 0:
                                    assignable = True
                            except ValueError:
                                assignable = True
                imports = [Ref(v, rel, n.line) for n in top.value if n.key == 'shared_focus' and isinstance((v := n.value), str)]
                if ident:
                    self.trees.setdefault(ident, Ref(ident, rel, top.line, {'assignable': assignable, 'imports': imports}))
                for focus in children(top.value, 'focus'):
                    if isinstance(focus, list) and child(focus, 'id'):
                        self.focuses.setdefault(child(focus, 'id'), Ref(child(focus, 'id'), rel, top.line, {'shared': False}))
            elif top.key == 'shared_focus':
                ident = child(top.value, 'id')
                if ident:
                    prereqs = set()
                    for pre in children(top.value, 'prerequisite'):
                        if isinstance(pre, list):
                            prereqs |= {v for n in pre if n.key == 'focus' and isinstance((v := n.value), str)}
                    self.shared_focuses.setdefault(ident, Ref(ident, rel, top.line, {'prerequisites': prereqs}))
                    self.focuses.setdefault(ident, Ref(ident, rel, top.line, {'shared': True}))

    def _walk(self, rel, nodes, path, reference):
        parent = path[-1] if path else None
        for position, node in enumerate(nodes):
            key, value = node.key, node.value
            if not key:
                if isinstance(value, list):
                    self._walk(rel, value, path + ['{'], reference)
                continue
            ref = Ref(key, rel, node.line)
            if reference:
                # Reference files contribute definitions only: flags and variables they set,
                # and the events they fire (callers of vanilla-namespace events kept by the mod).
                if key in FLAG_SET:
                    name = value if isinstance(value, str) else child(value, 'flag') if isinstance(value, list) else None
                    if isinstance(name, str):
                        self.flag_set[(FLAG_SET[key], unquote(name))].append(Ref(name, rel, node.line, {'reference': True}))
                if key in EVENT_TYPES:
                    ident = value if isinstance(value, str) else child(value, 'id') if isinstance(value, list) else None
                    if isinstance(ident, str):
                        self.event_calls[ident].append(Ref(ident, rel, node.line, {'reference': True}))
                elif key in ('events', 'random_events') and rel.startswith('common/on_actions/') and isinstance(value, list):
                    for item in value:
                        ident = item.key if item.op is None else item.value if isinstance(item.value, str) else None
                        if ident:
                            self.event_calls[ident].append(Ref(ident, rel, item.line, {'reference': True}))
                if isinstance(value, list):
                    self._walk(rel, value, path + [key], reference)
                continue
            if path:
                self.key_uses[key].append(ref)
            if key in FLAG_SET or key in FLAG_READ or key.startswith('clr_') and key.endswith('_flag'):
                name = value if isinstance(value, str) else child(value, 'flag') if isinstance(value, list) else None
                if isinstance(name, str):
                    name = unquote(name)
                    if key in FLAG_SET:
                        self.flag_set[(FLAG_SET[key], name)].append(Ref(name, rel, node.line))
                    elif key in FLAG_READ:
                        self.flag_read[(FLAG_READ[key], name)].append(Ref(name, rel, node.line))
                    else:
                        kind = key[4:-5]
                        kind = 'character' if kind in ('unit_leader', 'leader') else kind
                        self.flag_clear[(kind, name)].append(Ref(name, rel, node.line))
            if key in EVENT_TYPES:
                ident = value if isinstance(value, str) else child(value, 'id') if isinstance(value, list) else None
                if isinstance(ident, str):
                    self.event_calls[ident].append(ref)
            elif key in ('events', 'random_events') and rel.startswith('common/on_actions/') and isinstance(value, list):
                for item in value:
                    ident = item.key if item.op is None else item.value if isinstance(item.value, str) else None
                    if ident and re.match(r'^[A-Za-z0-9_]+\.\d+$', ident):
                        self.event_calls[ident].append(Ref(ident, rel, item.line, {'on_action': True}))
            if key in IDEA_USE:
                if key == 'idea' and parent not in ('add_timed_idea', 'modify_timed_idea', 'remove_timed_idea'):
                    pass
                else:
                    items = scalars(value) if key not in ('add_timed_idea', 'modify_timed_idea') else scalars(child(value, 'idea') if isinstance(value, list) else None)
                    for item in items:
                        if item not in ('yes', 'no'):
                            self.idea_uses[item].append(Ref(item, rel, node.line))
            if key == 'swap_ideas' and isinstance(value, list):
                for sub in ('remove_idea', 'add_idea'):
                    item = child(value, sub)
                    if isinstance(item, str):
                        self.idea_uses[item].append(Ref(item, rel, node.line))
            if key in ('activate_advisor', 'deactivate_advisor') and isinstance(value, str):
                self.idea_uses[value].append(Ref(value, rel, node.line, {'advisor': True}))
            if key in CHARACTER_USE:
                item = value if isinstance(value, str) else child(value, 'character') if isinstance(value, list) else None
                if isinstance(item, str) and not item.startswith(('ROOT', 'THIS', 'PREV', 'FROM', 'var:', '"')) and item not in ('yes', 'no'):
                    if key != 'character' or parent not in ('limit',):
                        self.character_uses[item].append(Ref(item, rel, node.line))
            if key in DECISION_USE:
                item = value if isinstance(value, str) else child(value, 'decision') if isinstance(value, list) else None
                if isinstance(item, str) and item not in ('yes', 'no') and not (key == 'decision' and parent not in ('activate_targeted_decision', 'remove_targeted_decision')):
                    self.decision_uses[item].append(Ref(item, rel, node.line))
            if key in CATEGORY_USE and isinstance(value, str):
                self.category_uses[value].append(ref)
            if key == 'load_focus_tree':
                tree = value if isinstance(value, str) else child(value, 'tree') if isinstance(value, list) else None
                if isinstance(tree, str):
                    self.tree_loads[tree].append(Ref(tree, rel, node.line))
            if key in VAR_SET:
                if isinstance(value, list):
                    target = child(value, 'var') or child(value, 'array')
                    names = [target] if isinstance(target, str) else [n.key for n in value[:1] if n.op == '=']
                    for name in names:
                        self.var_set[plain_var(name)].append(Ref(name, rel, node.line))
                elif isinstance(value, str):
                    self.var_set[plain_var(value)].append(Ref(value, rel, node.line))
            if key in ('check_variable', 'has_variable', 'is_in_array') or key == 'array' and parent in ('for_each_loop', 'for_each_scope_loop', 'any_of', 'all_of', 'any_of_scopes', 'all_of_scopes', 'random_scope_in_array'):
                if isinstance(value, str):
                    self.var_read[plain_var(value)].append(Ref(value, rel, node.line))
                elif isinstance(value, list):
                    target = child(value, 'var') or child(value, 'array')
                    if isinstance(target, str):
                        self.var_read[plain_var(target)].append(Ref(target, rel, node.line))
                    elif value and value[0].op in OPS and value[0].key not in ('value', 'compare', 'tooltip'):
                        self.var_read[plain_var(value[0].key)].append(Ref(value[0].key, rel, node.line))
            for token in (value,) if isinstance(value, str) else ():
                if token.startswith('var:'):
                    self.var_read[plain_var(token)].append(Ref(token, rel, node.line))
            if key in STATE_USE and isinstance(value, str) and value.isdigit():
                if key != 'state' or parent not in ('set_province_controller',):
                    self.state_uses[int(value)].append(ref)
            if key in PROVINCE_USE and isinstance(value, str) and value.isdigit():
                self.province_uses[int(value)].append(ref)
            elif key == 'province' and isinstance(value, list):
                for item in children(value, 'id'):
                    if isinstance(item, str) and item.isdigit():
                        self.province_uses[int(item)].append(ref)
            if key in ('if', 'else_if', 'else') and isinstance(value, list):
                body = [n for n in value if n.key not in ('limit',)]
                following = nodes[position + 1].key if position + 1 < len(nodes) else None
                context = Ref(key, rel, node.line, {'context': '/'.join(path[:1] + [key])})
                if not body and key == 'else':
                    self.empty_elses.append(context)
                elif not body and following not in ('else', 'else_if'):
                    # An empty if followed by else/else_if is the negation idiom: act only when the limit fails.
                    self.empty_ifs.append(context)
            if key == 'custom_effect_tooltip' and isinstance(value, str) and rel.startswith('events/'):
                self._want_loc(value, rel, node.line)
            if isinstance(value, list):
                self.scripted_calls.append((key, ref, {n.key for n in value if n.op}))
                self._walk(rel, value, path + [key], reference)
            elif value in ('yes', 'no'):
                self.scripted_calls.append((key, ref, set()))

    # ------------------------------------------------------------- helpers
    def owned(self, name):
        """The mod's own names: ac_*, TAG_* and the lower-case tag prefixes the archive used (sap_, geb_)."""
        head = name.split('_', 1)[0]
        if name.startswith('ac_') or head in self.tags:
            return True
        return head.upper() in self.tags and head.islower() and head not in COMMON_WORDS


def _flat(nodes):
    out = []
    for node in nodes:
        out.append(node.key)
        if isinstance(node.value, list):
            out.append(_flat(node.value))
        elif node.value is not None:
            out.append(node.value)
    return ' '.join(out)
