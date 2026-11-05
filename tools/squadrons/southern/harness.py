"""A small offline interpreter for compiled squadron-story scripts.

It executes the generated effects, triggers, events and on-actions of one
story component as text, exactly as compiled; the adapter supplies only the
calendar, country identity, war relations, capitulation, aircraft presence and
the published global flags a story reads. An unknown script key raises, so a
construct the interpreter does not model cannot pass silently. This is
offline evidence, not a native run.
"""
from datetime import date
from decimal import Decimal as D
from pathlib import Path
import re

TOKEN = re.compile(r'"[^"]*"|[{}]|[<>]=?|=|[^\s{}<>=]+')


def parse(text):
    tokens = TOKEN.findall(re.sub(r'#[^\n]*', '', text))
    position = 0

    def block():
        nonlocal position
        rows = []
        while position < len(tokens):
            token = tokens[position]
            if token == '}':
                position += 1
                return rows
            if position + 1 < len(tokens) and tokens[position + 1] in ('=', '<', '>', '<=', '>='):
                op = tokens[position + 1]
                position += 2
                if tokens[position] == '{':
                    position += 1
                    rows.append((token, op, block()))
                else:
                    rows.append((token, op, tokens[position].strip('"')))
                    position += 1
            else:
                rows.append((token, '', None))
                position += 1
        return rows
    return block()


def get(rows, key, default=None):
    for k, _, v in rows:
        if k == key:
            return v
    return default


def day(value):
    return date(*map(int, value.split('.'))).toordinal()


def localisation(text):
    result = {}
    for line in text.splitlines()[1:]:
        match = re.match(r'\s*([^\s:#]+):\d*\s+"(.*)"\s*$', line)
        if match:
            if match[1] in result:
                raise ValueError('Duplicate localisation key ' + match[1])
            result[match[1]] = match[2].replace('\\n', '\n').replace('\\"', '"')
    return result


class Country:
    def __init__(self, tag, ident):
        self.tag = self.original_tag = tag
        self.ident = ident
        self.exists = True
        self.capitulated = False
        self.air = True
        self.flags = {}
        self.variables = {}
        self.ideas = {}


class StoryWorld:
    def __init__(self, root, stem, namespace, tags, enabled=True):
        root = Path(root)

        def read(relative):
            return (root / relative).read_text(encoding='utf-8-sig')
        self.namespace = namespace
        self.enabled = enabled
        self.effects = dict((k, v) for k, _, v in parse(read('common/scripted_effects/' + stem + '.txt')))
        self.triggers = dict((k, v) for k, _, v in parse(read('common/scripted_triggers/' + stem + '.txt')))
        self.actions = get(parse(read('common/on_actions/' + stem + '.txt')), 'on_actions')
        self.events = {}
        for key, _, value in parse(read('events/' + stem + '.txt')):
            if key == 'country_event':
                if get(value, 'id') in self.events:
                    raise ValueError('Duplicate event ' + get(value, 'id'))
                self.events[get(value, 'id')] = value
        self.loc = localisation(read('localisation/english/' + stem + '_l_english.yml'))
        self.decisions = {}
        if (root / 'common/decisions' / (stem + '.txt')).exists():
            for category, _, rows in parse(read('common/decisions/' + stem + '.txt')):
                for key, _, value in rows:
                    self.decisions[key] = (category, value)
        self.countries = {tag: Country(tag, index + 1) for index, tag in enumerate(tags)}
        self.global_flags = set()
        self.wars = set()
        self.queue = []
        self.deliveries = []
        self.from_country = None
        self.today = day('1991.1.1')

    # -- calendar --------------------------------------------------------------------
    def at(self, when):
        self.today = day(when)
        return self

    def flag(self, country, name):
        expiry = country.flags.get(name, 0)
        return name in country.flags and (expiry is None or self.today < expiry)

    # -- triggers --------------------------------------------------------------------
    def number(self, value, c):
        if value == 'THIS.id':
            return D(c.ident)
        if value in ('deployed_airforce_manpower_k', 'num_deployed_planes'):
            return D(1 if c.air else 0)
        if re.fullmatch(r'-?\d+(\.\d+)?', value):
            return D(value)
        return c.variables.get(value, D(0))

    def compare(self, left, op, right):
        return {'=': left == right, '>': left > right, '<': left < right, '>=': left >= right, '<=': left <= right,
                'equals': left == right}[op]

    def trigger(self, nodes, c):
        for key, op, value in nodes:
            if not self.condition(key, op, value, c):
                return False
        return True

    def condition(self, key, op, value, c):
        if key == 'tag':
            return c.tag == value
        if key == 'original_tag':
            return c.original_tag == value
        if key == 'country_exists':
            return value in self.countries and self.countries[value].exists
        if key == 'has_country_flag':
            return self.flag(c, value)
        if key == 'has_global_flag':
            return value in self.global_flags
        if key == 'NOT':
            return not any(self.condition(k, o, v, c) for k, o, v in value)
        if key == 'OR':
            return any(self.condition(k, o, v, c) for k, o, v in value)
        if key == 'AND':
            return self.trigger(value, c)
        if key == 'date':
            return self.compare(self.today, op, day(value))
        if key == 'check_variable':
            if get(value, 'var') is not None:
                return self.compare(self.number(get(value, 'var'), c), get(value, 'compare', 'equals'), self.number(get(value, 'value'), c))
            name, inner, operand = value[0]
            return self.compare(self.number(name, c), inner, self.number(operand, c))
        if key == 'has_variable':
            return value in c.variables
        if key == 'has_game_rule':
            if get(value, 'rule') != 'ac_sq_stories' or get(value, 'option') != 'enabled':
                raise ValueError('Unknown story rule')
            return self.enabled
        if key == 'has_capitulated':
            return c.capitulated == (value == 'yes')
        if key == 'has_war':
            return any(c.tag in pair for pair in self.wars) == (value == 'yes')
        if key == 'has_war_with':
            return frozenset((c.tag, value)) in self.wars
        if key == 'always':
            return value == 'yes'
        if key in self.triggers:
            return self.trigger(self.triggers[key], c) == (value == 'yes')
        raise ValueError('Unmodelled trigger ' + key)

    # -- effects ---------------------------------------------------------------------
    def execute(self, nodes, c):
        branch = None
        for key, op, value in nodes:
            if key in ('if', 'else_if', 'else'):
                if key == 'if':
                    branch = False
                elif branch is None:
                    raise ValueError('Orphan conditional')
                if not branch and (key == 'else' or self.trigger(get(value, 'limit', []), c)):
                    self.execute([r for r in value if r[0] != 'limit'], c)
                    branch = True
                continue
            branch = None
            self.effect(key, op, value, c)

    def effect(self, key, op, value, c):
        if key == 'set_country_flag':
            if isinstance(value, list):
                c.flags[get(value, 'flag')] = self.today + int(get(value, 'days'))
            else:
                c.flags[value] = None
        elif key == 'clr_country_flag':
            c.flags.pop(value, None)
        elif key in ('set_variable', 'add_to_variable'):
            name, _, operand = value[0]
            amount = self.number(operand, c)
            c.variables[name] = amount if key == 'set_variable' else c.variables.get(name, D(0)) + amount
        elif key == 'clamp_variable':
            name = get(value, 'var')
            c.variables[name] = min(max(c.variables.get(name, D(0)), D(get(value, 'min'))), D(get(value, 'max')))
        elif key == 'country_event':
            self.queue.append((self.today + int(get(value, 'days', '0')), c.tag, get(value, 'id')))
        elif key == 'custom_effect_tooltip':
            if value not in self.loc:
                raise ValueError('Unlocalised tooltip ' + value)
        elif key == 'add_timed_idea':
            c.ideas[get(value, 'idea')] = self.today + int(get(value, 'days'))
        elif key == 'every_country':
            for other in self.countries.values():
                if other.exists and self.trigger(get(value, 'limit', []), other):
                    self.execute([r for r in value if r[0] != 'limit'], other)
        elif key == 'FROM':
            if self.from_country is not None:
                self.execute(value, self.from_country)
        elif key in self.effects:
            if value == 'yes':
                self.execute(self.effects[key], c)
        else:
            raise ValueError('Unmodelled effect ' + key)

    # -- engine adapters -------------------------------------------------------------
    def action(self, name, tag=None, other=None):
        prior = self.from_country
        self.from_country = self.countries.get(other)
        try:
            effect = get(get(self.actions, name), 'effect')
            if tag is None:
                self.execute(effect, None)
            else:
                self.execute(effect, self.countries[tag])
        finally:
            self.from_country = prior

    def descriptions(self, ident, c):
        result = []
        for key, _, value in self.events[ident]:
            if key == 'desc':
                if isinstance(value, str):
                    result.append(value)
                elif self.trigger(get(value, 'trigger', []), c):
                    result.append(get(value, 'text'))
        return result

    def options(self, ident):
        return [v for k, _, v in self.events[ident] if k == 'option']

    def deliver_due(self):
        """Deliver due events as the engine would, if their trigger still holds."""
        delivered = []
        for item in sorted(q for q in self.queue if q[0] <= self.today):
            self.queue.remove(item)
            _, tag, ident = item
            c = self.countries[tag]
            node = self.events[ident]
            if c.exists and self.trigger(get(node, 'trigger', []), c):
                self.execute(get(node, 'immediate', []), c)
                self.deliveries.append((tag, ident, self.descriptions(ident, c)))
                delivered.append((tag, ident))
        return delivered

    def choose(self, ident, index, tag):
        c = self.countries[tag]
        option = self.options(ident)[index]
        if not self.trigger(get(option, 'trigger', []), c):
            return False
        self.execute([r for r in option if r[0] not in ('name', 'trigger', 'ai_chance')], c)
        return True

    def week(self, tags):
        for tag in tags:
            if self.countries[tag].exists:
                self.action('on_weekly', tag)
        self.today += 7
        return self.deliver_due()
