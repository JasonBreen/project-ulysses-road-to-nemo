"""Compile one bespoke country spec into mod files.

compile_country(spec) returns {relative path: bytes}, a budget row and asset rows.
It validates the spec against the catalogue first and raises on the first
problem, so a writer gets one precise error at a time. Lint rules that judge
quality (filler, similarity, size) live in lint.py.
"""
import hashlib
import re
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path[:0] = [str(HERE), str(ROOT / 'tools/usea_depth'), str(ROOT / 'tools/usea_expansion')]
import art  # noqa: E402
import catalogue  # noqa: E402
import layout  # noqa: E402
import seams  # noqa: E402
import spec as S  # noqa: E402

INSTITUTIONAL_START = 12


def names(country):
    infix = 'ud' if country.root == 'usea' else 'wd'
    low = country.tag.lower()
    base = 'ac_%s_%s' % (infix, low)
    gfx = 'gfx/AC_usea_depth/%s' % country.package if country.root == 'usea' else 'gfx/AC_world_depth/%s' % low
    return dict(infix=infix, base=base, tree=base + '_tree', gfx=gfx,
                focus_file='common/national_focus/' + ('ac_ud_minor_%s.txt' % low if country.root == 'usea' else base + '.txt'),
                sprite='GFX_ac_%s_focus_' % infix)


def institutional_block():
    """The 36 shared regional focuses: (ids in order, {id: (x, y)})."""
    import importlib.util
    spec = importlib.util.spec_from_file_location('national_depth_institutions', ROOT / 'tools/institutions/content.py')
    institutions = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(institutions)
    ids = ['ac_reg_' + row.suffix for row in institutions.FOCUSES]
    return ids, {'ac_reg_' + row.suffix: (row.x, row.y) for row in institutions.FOCUSES}


def block(key, body):
    lines = body.rstrip('\n').split('\n') if body.strip() else []
    return key + ' = {\n' + ''.join('\t' + line + '\n' if line else '\n' for line in lines) + '}\n'


def quote(text):
    return text.replace('"', "'").replace('\n', '\\n')


class Compiler:
    def __init__(self, module):
        self.m = module
        self.c = module.COUNTRY
        self.n = names(self.c)
        self.loc = {}
        self.problems = []

    # --- identifiers ------------------------------------------------------------------------
    def fid(self, key):
        return '%s_%s_%s' % (self.c.tag, self.n['infix'], key)

    def event_id(self, key):
        index = [e.key for e in self.m.EVENTS].index(key) + 1
        return '%s.%d' % (self.n['base'], index)

    def office_id(self, key):
        return '%s_%s_%s_office' % (self.c.tag, self.n['infix'], key)

    def regime_name(self, key):
        return '%s_regime_%s' % (self.n['base'], key)

    # --- validation ---------------------------------------------------------------------------
    def require(self, condition, message):
        if not condition:
            raise ValueError('%s: %s' % (self.c.tag, message))

    def validate(self):
        m, c = self.m, self.c
        self.require(c.root in ('usea', 'world') and re.fullmatch(r'[A-Z]{3}', c.tag), 'bad country header')
        self.require(len(c.themes) == 3, 'three national picture subjects required')
        subjects = catalogue.subjects()
        parties = catalogue.ideologies()
        self.require(all(s in subjects for s in c.themes), 'unknown theme subject')
        keys = [f.key for b in m.BRANCHES for f in b.focuses]
        self.require(len(keys) == len(set(keys)), 'duplicate focus key')
        self.require(len({b.key for b in m.BRANCHES}) == len(m.BRANCHES), 'duplicate branch key')
        ideas = {i.key: i for i in m.IDEAS}
        events = {e.key for e in m.EVENTS}
        offices = {o.key: o for o in m.OFFICES}
        states, capital = catalogue.own_states(c.tag)
        self.require(capital in states, 'capital not among the 1991 states')
        for b in m.BRANCHES:
            self.require(b.filter in catalogue.FILTERS, b.key + ': unknown search filter ' + b.filter)
            self.require(1991 <= b.era <= 2020, b.key + ': era out of range')
            self.require(b.focuses, b.key + ': empty branch')
            for f in b.focuses:
                where = f.key
                self.require(re.fullmatch(r'[a-z][a-z0-9_]{2,40}', f.key), where + ': key must be snake_case')
                self.require(f.cost in (5, 10), where + ': cost must be 5 or 10')
                self.require(len(f.icon) == 2 and all(s in subjects for s in f.icon), where + ': unknown icon subject')
                for ref in (*f.after, *f.after_any, *f.exclusive):
                    self.require(ref in keys and ref != f.key, where + ': unknown focus reference ' + ref)
                for r in f.requires:
                    if isinstance(r, S.Completed):
                        self.require(r.focus in keys, where + ': unknown completed focus ' + r.focus)
                    elif isinstance(r, S.After):
                        self.require(re.fullmatch(r'\d{4}\.\d{1,2}\.\d{1,2}', r.date), where + ': bad date')
                    else:
                        self.require(isinstance(r, (S.HasFlag, S.NotFlag)), where + ': unknown requirement')
                for r in f.reward:
                    self.check_reward(r, where, ideas, events, offices, states)
                for text in (f.title, f.desc):
                    self.require(text.isascii() and '"' not in text, where + ': ASCII text without double quotes required')
        for i in m.IDEAS:
            self.require(i.modifiers, i.key + ': an idea needs at least one modifier')
            for k, v in i.modifiers.items():
                self.require(k in catalogue.MODIFIERS, i.key + ': unknown modifier ' + k)
                self.require(abs(v) <= catalogue.MODIFIERS[k], i.key + ': %s beyond %s' % (k, catalogue.MODIFIERS[k]))
            self.require(all(s in subjects for s in i.icon), i.key + ': unknown icon subject')
        for e in m.EVENTS:
            text = seams.event_text(e.paragraphs, e.layer, e.citation)
            self.require(not seams.event_problems(text), e.key + ': ' + ', '.join(seams.event_problems(text)))
            self.require(1 <= len(e.options) <= 4 and 0 <= e.picture <= 2, e.key + ': options or picture out of range')
            for o in e.options:
                for r in o.effects:
                    self.check_reward(r, e.key, ideas, events, offices, states)
        for o in m.OFFICES:
            self.require(o.party in parties and o.ideology in parties[o.party], o.key + ': unknown party or sub-ideology')
        self.require(all(s.layer in catalogue.LAYERS for s in m.SOURCES) and m.SOURCES, 'sources need a known layer')

    def check_reward(self, r, where, ideas, events, offices, states):
        if isinstance(r, (S.Idea, S.RemoveIdea, S.TimedIdea)):
            self.require(r.key in ideas, where + ': unknown idea ' + r.key)
        elif isinstance(r, S.SwapIdea):
            self.require(r.old in ideas and r.new in ideas, where + ': unknown idea in swap')
        elif isinstance(r, S.Build):
            self.require(r.kind in catalogue.BUILDINGS and 1 <= r.level <= 3, where + ': bad building')
            self.require(r.state == 0 or r.state in states, where + ': building outside the 1991 states')
        elif isinstance(r, S.Research):
            self.require(r.category in catalogue.TECH_CATEGORIES and 0 < r.bonus <= 1 and 1 <= r.uses <= 2, where + ': bad research bonus')
        elif isinstance(r, S.PP):
            self.require(-100 <= r.amount <= 150, where + ': political power out of range')
        elif isinstance(r, (S.Stability, S.WarSupport)):
            self.require(-0.15 <= r.amount <= 0.15, where + ': stability/war support out of range')
        elif isinstance(r, S.XP):
            self.require(r.kind in catalogue.XP_KINDS and 0 < r.amount <= 50, where + ': bad experience')
        elif isinstance(r, S.Event):
            self.require(r.key in events and 0 <= r.days <= 60, where + ': unknown event ' + r.key)
        elif isinstance(r, S.Flag):
            self.require(re.fullmatch(r'[a-z][a-z0-9_]{2,40}', r.name), where + ': bad flag name')
        elif isinstance(r, S.Regime):
            self.require(r.office in offices, where + ': unknown office ' + r.office)
        elif isinstance(r, S.Tooltip):
            self.require(r.text.isascii() and '"' not in r.text, where + ': bad tooltip')
        else:
            raise ValueError('%s: %s: reward not in the catalogue: %r' % (self.c.tag, where, r))

    # --- rendering ------------------------------------------------------------------------------
    def reward(self, r, owner, index):
        if isinstance(r, S.Idea):
            return 'add_ideas = %s\n' % self.fid(r.key)
        if isinstance(r, S.SwapIdea):
            return block('swap_ideas', 'remove_idea = %s\nadd_idea = %s' % (self.fid(r.old), self.fid(r.new)))
        if isinstance(r, S.RemoveIdea):
            return 'remove_ideas = %s\n' % self.fid(r.key)
        if isinstance(r, S.TimedIdea):
            return block('add_timed_idea', 'idea = %s\ndays = %d' % (self.fid(r.key), r.days))
        if isinstance(r, S.Build):
            build = block('add_building_construction', 'type = %s\nlevel = %d\ninstant_build = yes' % (r.kind, r.level))
            if r.state == 0:
                return block('capital_scope', build)
            return block('if', block('limit', 'owns_state = %d' % r.state) + block(str(r.state), build))
        if isinstance(r, S.Research):
            return block('add_tech_bonus', 'name = %s\nbonus = %s\nuses = %d\ncategory = %s' % (owner, r.bonus, r.uses, r.category))
        if isinstance(r, S.PP):
            return 'add_political_power = %d\n' % r.amount
        if isinstance(r, S.Stability):
            return 'add_stability = %s\n' % r.amount
        if isinstance(r, S.WarSupport):
            return 'add_war_support = %s\n' % r.amount
        if isinstance(r, S.XP):
            return '%s = %d\n' % (catalogue.XP_KINDS[r.kind], r.amount)
        if isinstance(r, S.Event):
            return block('country_event', 'id = %s\ndays = %d' % (self.event_id(r.key), r.days))
        if isinstance(r, S.Flag):
            return 'set_country_flag = %s\n' % self.fid(r.name)
        if isinstance(r, S.Regime):
            return '%s = yes\n' % self.regime_name(r.office)
        if isinstance(r, S.Tooltip):
            key = '%s_tt_%d' % (owner, index)
            self.loc[key] = r.text
            return 'custom_effect_tooltip = %s\n' % key
        raise ValueError(repr(r))

    def requirement(self, r):
        if isinstance(r, S.HasFlag):
            return 'has_country_flag = %s' % self.fid(r.name)
        if isinstance(r, S.NotFlag):
            return 'NOT = { has_country_flag = %s }' % self.fid(r.name)
        if isinstance(r, S.Completed):
            return 'has_completed_focus = %s' % self.fid(r.focus)
        return 'date > %s' % r.date

    def compile(self):
        self.validate()
        m, c, n = self.m, self.c, self.n
        geometry = __import__('focus_layout').gui_geometry()
        positions, lanes = layout.place(m.BRANCHES, c.max_columns, INSTITUTIONAL_START)
        reg_ids, reg_positions = institutional_block()
        exclusive = {}
        for b in m.BRANCHES:
            for f in b.focuses:
                for other in f.exclusive:
                    exclusive.setdefault(f.key, set()).add(other)
                    exclusive.setdefault(other, set()).add(f.key)
        regime_focus = {f.key for b in m.BRANCHES for f in b.focuses if any(isinstance(r, S.Regime) for r in f.reward)}
        focuses, sprites, assets, outputs = [], [], [], {}
        icon_count = {}
        for b in m.BRANCHES:
            for f in b.focuses:
                ident = self.fid(f.key)
                self.loc[ident] = f.title
                self.loc[ident + '_desc'] = f.desc
                x, y = positions[f.key]
                body = 'id = %s\nicon = %s%s\nx = %d\ny = %d\ncost = %d\n' % (ident, n['sprite'], ident, x, y, f.cost)
                for parent in f.after:
                    body += block('prerequisite', 'focus = %s' % self.fid(parent))
                if f.after_any:
                    body += block('prerequisite', '\n'.join('focus = %s' % self.fid(p) for p in f.after_any))
                if f.key in exclusive:
                    body += block('mutually_exclusive', '\n'.join('focus = %s' % self.fid(k) for k in sorted(exclusive[f.key])))
                conditions = ['NOT = { date < %d.1.1 }' % b.era] + [self.requirement(r) for r in f.requires]
                body += block('available', '\n'.join(conditions))
                body += block('search_filters', b.filter)
                body += block('ai_will_do', 'factor = %d' % (0 if f.key in regime_focus else f.ai))
                body += block('completion_reward', ''.join(self.reward(r, ident, i) for i, r in enumerate(f.reward)))
                focuses.append(block('focus', body))
                pair = tuple(f.icon)
                arrangement = icon_count.get(pair, 0)
                icon_count[pair] = arrangement + 1
                self.require(arrangement < len(art.ARRANGEMENTS), f.key + ': too many icons with subjects %s; vary them' % (pair,))
                relative = '%s/focus/%s.dds' % (n['gfx'], ident)
                outputs[relative] = art.encoded(art.focus_icon(c.tag, f.icon[0], f.icon[1], arrangement, mark=f.cost == 10))
                sprites.append('spriteType = { name = "%s%s" texturefile = "%s" }' % (n['sprite'], ident, relative))
                sprites.append('spriteType = { name = "%s%s_shine" texturefile = "%s" }' % (n['sprite'], ident, relative))
                assets.append(dict(id=ident, file=relative, kind='focus', subjects=list(f.icon), arrangement=arrangement))
        all_positions = dict(reg_positions)
        all_positions.update({self.fid(k): v for k, v in positions.items()})
        import focus_layout
        panel = focus_layout.panel_position(all_positions, geometry)
        first = self.fid(m.BRANCHES[0].focuses[0].key)
        header = ('id = %s\ncountry = { factor = 0 modifier = { add = 50 tag = %s original_tag = %s } }\ndefault = no\n'
                  'reset_on_civilwar = no\ninitial_show_position = { focus = %s }\ncontinuous_focus_position = { x = %d y = %d }\n'
                  % (n['tree'], c.tag, c.tag, first, panel[0], panel[1]))
        header += '# The shared institutional programme (tools/institutions), unchanged.\n'
        header += ''.join('shared_focus = %s\n' % i for i in reg_ids)
        tree = block('focus_tree', header + '\n'.join(focuses))
        provenance = '# Bespoke national tree; source: tools/national_depth (%s). Provisional gameplay unless a ledger row says otherwise. Native acceptance pending.\n' % c.name
        outputs[n['focus_file']] = (provenance + tree).encode('utf-8')
        self.loc[n['tree']] = c.name + ': National Programme'
        # ideas
        idea_rows = ''
        for i in m.IDEAS:
            ident = self.fid(i.key)
            self.loc[ident] = i.title
            self.loc[ident + '_desc'] = i.desc
            mods = ''.join('%s = %s\n' % (k, v) for k, v in i.modifiers.items())
            idea_rows += block(ident, 'picture = %s\nallowed = { always = no }\nremoval_cost = -1\n' % ident + block('modifier', mods))
            relative = '%s/ideas/%s.dds' % (n['gfx'], ident)
            outputs[relative] = art.encoded(art.idea_icon(c.tag, i.icon[0], i.icon[1]))
            sprites.append('spriteType = { name = "GFX_idea_%s" texturefile = "%s" }' % (ident, relative))
            assets.append(dict(id=ident, file=relative, kind='idea', subjects=list(i.icon)))
        if m.IDEAS:
            outputs['common/ideas/%s.txt' % n['base']] = (provenance + block('ideas', block('country', idea_rows))).encode('utf-8')
        # national pictures and events
        themes = c.themes
        pairs = [(themes[0], themes[1]), (themes[1], themes[2]), (themes[2], themes[0])]
        for index, pair in enumerate(pairs):
            relative = '%s/events/%s_%d.dds' % (n['gfx'], n['base'], index)
            outputs[relative] = art.encoded(art.event_picture(c.tag, pair))
            sprites.append('spriteType = { name = "GFX_%s_event_%d" texturefile = "%s" }' % (n['base'], index, relative))
            assets.append(dict(id='%s_event_%d' % (n['base'], index), file=relative, kind='event picture', subjects=list(pair)))
        events = ''
        for e in m.EVENTS:
            ident = self.event_id(e.key)
            self.loc[ident + '.t'] = e.title
            self.loc[ident + '.d'] = seams.event_text(e.paragraphs, e.layer, e.citation)
            options = ''
            for k, o in enumerate(e.options):
                name = '%s.%s' % (ident, 'abcd'[k])
                self.loc[name] = o.title
                options += block('option', 'name = %s\n' % name + block('ai_chance', 'base = %d' % o.ai) +
                                 ''.join(self.reward(r, name.replace('.', '_'), i) for i, r in enumerate(o.effects)))
            events += block('country_event', 'id = %s\ntitle = %s.t\ndesc = %s.d\npicture = GFX_%s_event_%d\nis_triggered_only = yes\n'
                            % (ident, ident, ident, n['base'], e.picture) + options)
        if m.EVENTS:
            outputs['events/%s.txt' % n['base']] = (provenance + 'add_namespace = %s\n\n' % n['base'] + events).encode('utf-8')
        # offices and regimes
        effects, characters = '', ''
        for o in m.OFFICES:
            ident = self.office_id(o.key)
            self.loc[ident] = o.title
            self.loc[ident + '_desc'] = o.desc
            relative = '%s/offices/%s.dds' % (n['gfx'], ident)
            outputs[relative] = art.encoded(art.portrait(c.tag, themes[0]))
            assets.append(dict(id=ident, file=relative, kind='office card', subjects=[themes[0]]))
            characters += block(ident, 'name = %s\n' % ident + block('portraits', block('civilian', 'large = "%s"' % relative)) +
                                block('country_leader', 'ideology = %s\ntraits = { }\nexpire = "2066.1.1.1"\ndesc = %s_desc' % (o.ideology, ident)))
            lines = 'set_politics = { ruling_party = %s elections_allowed = %s }\n' % (o.party, 'yes' if o.elections else 'no')
            lines += 'if = { limit = { NOT = { has_character = %s } } recruit_character = %s }\n' % (ident, ident)
            lines += 'promote_character = { character = %s ideology = %s }\n' % (ident, o.ideology)
            effects += block(self.regime_name(o.key), lines)
        if m.OFFICES:
            outputs['common/characters/%s.txt' % n['base']] = (provenance + block('characters', characters)).encode('utf-8')
            outputs['common/scripted_effects/%s.txt' % n['base']] = (provenance + effects).encode('utf-8')
        # readable flag labels
        for flag in sorted({r.name for b in m.BRANCHES for f in b.focuses for r in f.reward if isinstance(r, S.Flag)} |
                           {r.name for e in m.EVENTS for o in e.options for r in o.effects if isinstance(r, S.Flag)}):
            self.loc[self.fid(flag)] = '%s: %s' % (c.name, flag.replace('_', ' ').capitalize())
        outputs['interface/%s.gfx' % n['base']] = block('spriteTypes', '\n'.join(sprites)).encode('utf-8')
        yml = 'l_english:\n' + ''.join(' %s:0 "%s"\n' % (k, quote(v)) for k, v in self.loc.items())
        outputs['localisation/english/%s_l_english.yml' % n['base']] = b'\xef\xbb\xbf' + yml.encode('utf-8')
        own = sum(len(b.focuses) for b in m.BRANCHES)
        budget = dict(tag=c.tag, tree=n['tree'], own_focuses=own, shared_focuses=len(reg_ids), total=own + len(reg_ids),
                      events=len(m.EVENTS), ideas=len(m.IDEAS), offices=len(m.OFFICES), panel=list(panel), lanes=len(lanes))
        for row in assets:
            row['sha256'] = hashlib.sha256(outputs[row['file']]).hexdigest()
        return outputs, budget, assets, positions


def compile_country(module):
    return Compiler(module).compile()
