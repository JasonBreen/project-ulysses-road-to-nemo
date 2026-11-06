"""Bound the original engine-owned country picker, without changing bindings.

The captured pre-repair blocks are provenance, not an acceptance fingerprint.
Acceptance evaluates actual rectangles, scrolling, frame extents and controls.
"""
import argparse
import copy
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MOD = ROOT / 'mod/2985041246'
sys.path.insert(0, str(ROOT / 'tools/usea_expansion'))
from script import get, parse, render, setv, walk, xy

CONTRACT = HERE / 'responsive_original.json'
MANAGED = ('bookmark_entry', 'country_entry', 'country_entry_medium',
           'country_entry_mini', 'gamesetup_scenario_window',
           'gamesetup_interesting_countries_window', 'gamesetup_country_details')
VIEWPORTS = [(3440, 1440, s) for s in (1, 1.25, 1.5)] + [
    (w, h, s) for w, h in ((2560, 1440), (1920, 1080)) for s in (1, 1.25)
] + [(1280, 720, 1)]


def span(text, name):
    matches = list(re.finditer(r'\bname\s*=\s*"' + re.escape(name) + '"', text))
    if len(matches) != 1:
        raise ValueError('Missing or ambiguous control: ' + name)
    start = text.rfind('containerWindowType', 0, matches[0].start())
    if start < 0:
        raise ValueError('Missing window: ' + name)
    depth = 0
    for token in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]', text[start:]):
        if token[0] == '{':
            depth += 1
        elif token[0] == '}':
            depth -= 1
            if depth == 0:
                return start, start + token.end()
    raise ValueError('Unclosed window: ' + name)


def named(node, name):
    matches = [n for _, n in walk(node) if get(n, 'name', '').strip('"') == name]
    if len(matches) != 1:
        raise ValueError('Missing or duplicate child control: ' + name)
    return matches[0]


def size(node, w, h):
    setv(node, 'size', [['width', '=', str(w)], ['height', '=', str(h)]])


def move(node, x, y):
    setv(node, 'position', xy(x, y))


def text(node, x, y, w, h, font='Aces16'):
    move(node, x, y)
    setv(node, 'maxWidth', str(w))
    setv(node, 'maxHeight', str(h))
    setv(node, 'font', '"' + font + '"')


def repair(name, node):
    """Modify existing nodes so unknown compatibility children are retained."""
    if name == 'bookmark_entry':
        size(node, 232, 211)
        text(named(node, 'date'), 16, 170, 200, 24)
    elif name == 'country_entry':
        size(node, 138, 108)
        leader = named(node, 'country_leader')
        move(leader, 8, 5)
        setv(leader, 'scale', '0.30')
        flag = named(node, 'country_flag')
        move(flag, 70, 15)
        setv(flag, 'scale', '0.60')
        setv(named(node, 'country'), 'quadTextureSprite', '"GFX_ac_briefing_country_entry"')
        text(named(node, 'country_name'), 4, 78, 130, 30, 'Aces14')
    elif name == 'country_entry_medium':
        size(node, 138, 97)
    elif name == 'country_entry_mini':
        size(node, 59, 44)
    elif name == 'gamesetup_scenario_window':
        size(node, 780, 620)
        setv(node, 'moveable', 'no')
        text(named(node, 'title'), 20, 14, 740, 30, 'Aces20')
        bookmarks = named(node, 'bookmarks')
        move(bookmarks, 130, 60)
        size(bookmarks, 520, 220)
        grid = named(bookmarks, 'bookmarks_grid')
        move(grid, 0, 0)
        size(grid, 520, 220)
        setv(grid, 'slotsize', [['width', '=', '250'], ['height', '=', '211']])
        text(named(node, 'history_title'), 20, 294, 740, 24)
        text(named(node, 'bookmark_title'), 30, 328, 720, 28, 'Aces20')
        desc = named(node, 'bookmark_desc')
        text(desc, 30, 366, 710, 170)
        setv(desc, 'scrollbarType', '"ac_exp_standardtext_slider"')
        for control, x in [('back_button', 30), ('select_button', 528)]:
            button = named(node, control)
            move(button, x, 564)
            setv(button, 'Orientation', '"UPPER_LEFT"')
            setv(button, 'buttonFont', '"Aces16"')
    elif name == 'gamesetup_interesting_countries_window':
        size(node, 1200, 660)
        move(node, 0, 0)
        setv(node, 'moveable', 'no')
        move(named(node, 'single_player_country_bg'), 0, 0)
        overview = named(node, 'ac_overhaul_world_overview')
        move(overview, 20, 50)
        setv(overview, 'scale', '0.45')
        text(named(node, 'ac_overhaul_overview_title'), 20, 14, 540, 26)
        text(named(node, 'ac_overhaul_overview_note'), 20, 326, 540, 36, 'Aces14')
        for control, y, height, slot_w, slot_h in [
                ('countries', 50, 110, 145, 108),
                ('countries_medium', 165, 97, 145, 97),
                ('countries_mini', 274, 88, 59, 44)]:
            holder = named(node, control)
            move(holder, 590, y)
            size(holder, 590, height)
            setv(holder, 'clipping', 'yes')
            setv(holder, 'verticalScrollbar', '"ac_exp_right_vertical_slider"')
            setv(holder, 'scroll_wheel_factor', '44')
            setv(holder, 'smooth_scrolling', 'yes')
            grid = named(holder, 'countries_grid')
            size(grid, 590, height)
            setv(grid, 'slotsize', [['width', '=', str(slot_w)], ['height', '=', str(slot_h)]])
            grid[:] = [r for r in grid if r[0] not in ('max_slots_horizontal', 'max_slots_vertical')]
            grid.append(['max_slots_horizontal', '=', '10' if control == 'countries_mini' else '4'])
            setv(grid, 'max_slots_vertical', '0')
        text(named(node, 'nation_title'), 590, 12, 580, 32, 'Aces20')
        text(named(node, 'history_title'), 20, 372, 520, 24)
        history = named(node, 'history')
        text(history, 20, 405, 520, 180)
        setv(history, 'scrollbarType', '"ac_exp_standardtext_slider"')
        text(named(node, 'info_title'), 560, 372, 300, 24)
        info = named(node, 'info')
        move(info, 560, 405)
        for _, child in walk(info):
            if get(child, 'maxWidth'):
                setv(child, 'maxWidth', '280')
                setv(child, 'maxHeight', '20')
        leader = named(node, 'minor_country_leader')
        move(leader, 1080, 350)
        setv(leader, 'scale', '0.35')
        setv(leader, 'rotation', '0')
        frame = named(node, 'minor_portrait_overlay')
        move(frame, 1075, 345)
        setv(frame, 'scale', '0.50')
        spirit = named(node, 'spirit')
        move(spirit, 890, 438)
        setv(named(spirit, 'pol_faction_icon'), 'scale', '0.65')
        ideas = named(spirit, 'ideas')
        move(ideas, 50, 0)
        size(ideas, 240, 70)
        size(named(ideas, 'ideas_grid'), 240, 70)
        focus = named(spirit, 'focus')
        move(focus, 0, 76)
        size(focus, 280, 85)
        grid = named(focus, 'focus_grid')
        move(grid, 0, 0)
        size(grid, 280, 85)
        setv(grid, 'slotsize', [['width', '=', '70'], ['height', '=', '80']])
        for control, x in [('back_button', 20), ('select_button', 1032)]:
            button = named(node, control)
            move(button, x, 610)
            setv(button, 'Orientation', '"UPPER_LEFT"')
            setv(button, 'buttonFont', '"Aces16"')
    elif name == 'gamesetup_country_details':
        move(node, -20, -490)
        setv(node, 'show_position', xy(-20, 90))
        for name in ('spirit_grid', 'spirit_grid_over_defined'):
            grid = named(node, name)
            move(grid, 245, 28)
            size(grid, 225, 68)
    return node


def build(text):
    for name in MANAGED:
        start, end = span(text, name)
        row = parse(text[start:end])[0]
        row[2] = repair(name, row[2])
        text = text[:start] + render([row]) + text[end:]
    return text


def validate(text):
    windows = {name: parse(text[slice(*span(text, name))])[0][2] for name in MANAGED}
    errors = []
    def require(ok, message):
        if not ok:
            errors.append(message)
    for name, w, h in [('gamesetup_scenario_window', 780, 620),
                       ('gamesetup_interesting_countries_window', 1200, 660)]:
        node = windows[name]
        require((get(get(node, 'size'), 'width'), get(get(node, 'size'), 'height')) == (str(w), str(h)), name + ' dimensions')
        for vw, vh, scale in VIEWPORTS:
            require(w <= vw / scale - 40 and h <= vh / scale - 40,
                    f'{name} exceeds safe viewport {vw}x{vh}@{scale}')
        for control in ('back_button', 'select_button'):
            button = named(node, control)
            x, y = (int(get(get(button, 'position'), k)) for k in ('x', 'y'))
            bw = 221 if 'scenario' in name else 148
            require(0 <= x <= w - bw and 0 <= y <= h - 36, name + '/' + control + ' is clipped')
        require(get(named(node, 'back_button'), 'shortcut') == '"ESCAPE"', name + ' Escape binding')
        require(get(named(node, 'select_button'), 'shortcut') == '"RETURN"', name + ' Return binding')
    scenario = windows['gamesetup_scenario_window']
    grid = named(scenario, 'bookmarks_grid')
    require(get(get(grid, 'slotsize'), 'width') == '250', 'Bookmark slots must be finite')
    require(2 * 250 <= 520, 'Both 1991 bookmarks must fit')
    desc = named(scenario, 'bookmark_desc')
    require(get(desc, 'scrollbarType') == '"ac_exp_standardtext_slider"', 'Scenario prose must scroll')
    country = windows['gamesetup_interesting_countries_window']
    history = named(country, 'history')
    require(get(history, 'scrollbarType') == '"ac_exp_standardtext_slider"', 'Country prose must scroll')
    require(405 + int(get(history, 'maxHeight')) < 610, 'Country prose overlaps footer')
    require(50 + 594 * float(get(named(country, 'ac_overhaul_world_overview'), 'scale')) < 326, 'Map overlaps overview note')
    for name in ('countries', 'countries_medium', 'countries_mini'):
        holder = named(country, name)
        require(get(holder, 'clipping') == 'yes' and get(holder, 'verticalScrollbar') is not None, 'Unbounded country list: ' + name)
    # Compare the engine binding inventory, independently of positions/style.
    if CONTRACT.exists():
        original = json.loads(CONTRACT.read_text())
        for name, node in windows.items():
            prior = parse(original['blocks'][name])[0][2]
            names = lambda n: sorted(get(child, 'name') for _, child in walk(n) if get(child, 'name'))
            require(names(prior) == names(node), 'Engine controls changed: ' + name)
            require(repair(name, copy.deepcopy(prior)) == node,
                    'Control differs from the reviewed responsive specification: ' + name)
    return errors


def restore_historical(text):
    errors = validate(text)
    if errors:
        raise ValueError('; '.join(errors))
    contract = json.loads(CONTRACT.read_text())
    for name, original in contract['blocks'].items():
        start, end = span(text, name)
        text = text[:start] + original + text[end:]
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--capture', action='store_true')
    args = parser.parse_args()
    target = MOD / 'interface/frontendgamesetupview.gui'
    original = target.read_text(encoding='utf-8-sig')
    if args.capture:
        if CONTRACT.exists():
            raise SystemExit('Refusing to replace the pre-repair provenance')
        CONTRACT.write_text(json.dumps(dict(schema=1, base='38c978d0', blocks={
            name: original[slice(*span(original, name))] for name in MANAGED}), indent=2) + '\n', encoding='utf-8')
    result = build(original)
    errors = validate(result)
    if errors:
        raise SystemExit('\n'.join(errors))
    if args.check:
        if result != original:
            raise SystemExit('Responsive frontend differs from its authoring source')
    else:
        target.write_text(result, encoding='utf-8', newline='\n')
    print('Responsive frontend: both 1991 bookmarks; 8 viewport/scale cases; bindings preserved; native pending.')


if __name__ == '__main__':
    main()
