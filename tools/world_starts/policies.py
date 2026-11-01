"""Effective history laws/ideas used by conservative physical-start worksheets."""
from collections import Counter
from pathlib import Path
from script import parse, get
from inventory import selected

KEYS = {'min_export', 'local_resources_factor', 'resources_factor', 'resource_gain_efficiency',
        'fuel_gain_factor', 'industrial_capacity_factory', 'industrial_capacity_dockyard',
        'production_factory_efficiency_gain_factor', 'consumer_goods_expected_value',
        'consumer_goods_factor', 'conscription', 'conscription_factor', 'non_core_manpower',
        'local_factories', 'local_building_slots_factor', 'fuel_gain_factor_from_states', 'max_fuel_factor', 'max_fuel'}


def history_signature(source, tag, dlcs=(), human_tags=()):
    return [[key, [k for k, _, _ in value] if isinstance(value, list) else [value]]
            for key, _, value in selected(parse(source), set(dlcs), tag, human_tags) if key in ('add_ideas', 'remove_ideas')]


def catalog(engine):
    if hasattr(engine, '_start_ideas'): return engine._start_ideas
    paths = {p.name: p for p in (engine.reference / 'common/ideas').glob('*.txt')}
    paths.update({p.name: p for p in (Path(__file__).resolve().parents[2] / 'mod/2985041246/common/ideas').glob('*.txt')})
    ideas = {}; groups = {}; defaults = {}; unparsed = []
    for path in sorted(paths.values(), key=lambda p: (p.name.casefold(), p.name)):
        try:
            tree = parse(path.read_text(encoding='utf-8-sig'))
        except ValueError as exc:
            # Some unrelated engine country files use preprocessing grammar
            # beyond this offline parser. A required unresolved idea still
            # fails below; this is never a zero-modifier waiver for active IDs.
            unparsed.append(dict(file=path.name, parser_error=str(exc)))
            continue
        for category, _, entries in get(tree, 'ideas', []):
            if not isinstance(entries, list): continue
            for ident, _, body in entries:
                if not isinstance(body, list): continue
                ideas[ident] = (body, path); groups[ident] = category
                if get(entries, 'law') == 'yes' and get(body, 'default') == 'yes': defaults[category] = ident
    engine._start_ideas = ideas, groups, defaults, unparsed
    return engine._start_ideas


def capture(source, tag, engine, dlcs=(), human_tags=()):
    ideas, groups, defaults, unparsed = catalog(engine)
    active = set(defaults.values()); chosen = dict(defaults)
    for key, _, value in selected(parse(source), set(dlcs), tag, human_tags):
        if key not in ('add_ideas', 'remove_ideas'): continue
        names = [k for k, _, _ in value] if isinstance(value, list) else [value]
        for ident in names:
            if key == 'remove_ideas': active.discard(ident); continue
            if ident not in ideas: raise ValueError('Unresolved starting policy: ' + tag + ':' + ident)
            category = groups[ident]
            if category in defaults:
                active.discard(chosen[category]); chosen[category] = ident
            active.add(ident)
    modifiers = Counter(); negative = Counter(); rows = []
    for ident in sorted(active):
        body, path = ideas[ident]; engine.record(path)
        values = {k: float(v) for k, _, v in get(body, 'modifier', []) if k in KEYS}
        modifiers.update(values); negative.update({k: min(0, v) for k, v in values.items()})
        rows.append(dict(idea=ident, category=groups[ident], modifiers=values))
    return dict(laws=chosen, active_ideas=rows, modifiers=dict(modifiers), negative_modifiers=dict(negative),
                history_policy_signature=history_signature(source, tag, dlcs, human_tags),
                unparsed_unreferenced_primary_files=unparsed,
                coverage='Direct history/default laws and literal idea modifiers; later decisions, dynamic modifiers and native mobilization timing remain separate.')
